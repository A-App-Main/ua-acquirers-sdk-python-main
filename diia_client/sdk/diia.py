from typing import List, Optional, Sequence

from diia_client.crypto.base_service import AbstractCryptoService
from diia_client.enums import DiiaIDAction, DocumentType
from diia_client.sdk.http.base_client import AbstractHTTPCLient
from diia_client.sdk.model import (
    AuthDeepLink,
    DocumentPackage,
    EncodedFile,
    File,
    SignaturePackage,
)
from diia_client.sdk.remote.diia_api import DiiaApi
from diia_client.sdk.remote.model import Branch, BranchList, Offer, OfferList
from diia_client.sdk.service.branch_service import BranchService
from diia_client.sdk.service.document_service import DocumentService
from diia_client.sdk.service.offer_service import OfferService
from diia_client.sdk.service.sharing_service import SharingService
from diia_client.sdk.service.sign_service import SignService
from diia_client.sdk.service.validation_service import ValidationService
from diia_client.types import StrDict


class Diia:
    def __init__(
        self,
        *,
        acquirer_token: str,
        auth_acquirer_token: str,
        diia_host: str,
        http_client: AbstractHTTPCLient,
        crypto_service: AbstractCryptoService,
    ) -> None:
        """Main Diia class constructor.

        Args:
            acquirer_token: A token used to identify the Partner.
            diia_host: Base URL to Diia REST API.
            http_client: Preconfigured implementation of AbstractHTTPCLient.
            crypto_service: Preconfigured implementation of AbstractCryptoService.

        """
        diia_api = DiiaApi(
            acquirer_token=acquirer_token,
            auth_acquirer_token=auth_acquirer_token,
            diia_host=diia_host,
            http_client=http_client,
        )

        self.document_service = DocumentService(crypto_service)
        self.sharing_service = SharingService(diia_api=diia_api)
        self.branch_service = BranchService(diia_api=diia_api)
        self.offer_service = OfferService(diia_api=diia_api)
        self.validation_service = ValidationService(diia_api=diia_api)
        self.sign_service = SignService(
            diia_api=diia_api, crypto_service=crypto_service
        )

    def get_branches(
        self, *, skip: Optional[int] = None, limit: Optional[int] = None
    ) -> BranchList:
        """Get branches list.

        Args:
            skip: Number of branches to be skipped.
            limit: Max number of branches in response.

        Raises:
            DiiaClientException
        """
        return self.branch_service.get_branches(skip=skip, limit=limit)

    def get_branch(self, branch_id: str) -> Branch:
        """Get branch by id.

        Args:
            branch_id: Branch ID.

        Raises:
            DiiaClientException
        """
        return self.branch_service.get_branch(branch_id)

    def delete_branch(self, branch_id: str) -> None:
        """Delete branch.

        Args:
            branch_id: Branch ID.

        Raises:
            DiiaClientException
        """
        return self.branch_service.delete_branch(branch_id)

    def create_branch(
        self,
        name: str,
        email: str,
        region: str,
        district: str,
        location: str,
        street: str,
        house: str,
        custom_full_name: Optional[str] = None,
        custom_full_address: Optional[str] = None,
        sharing: Optional[List[DocumentType]] = None,
        document_identification: Optional[List[DocumentType]] = None,
        identification: Optional[List[str]] = None,
        diia_id: Optional[List[DiiaIDAction]] = None,
        delivery_types: Sequence[str] = ("api",),
        offer_request_type: str = "dynamic",
    ) -> Branch:
        """Create new branch.

        Returns:
            Created branch.

        Raises:
            pydantic.ValidationError, DiiaClientException
        """
        return self.branch_service.create_branch(
            name=name,
            email=email,
            region=region,
            district=district,
            location=location,
            street=street,
            house=house,
            sharing=sharing,
            document_identification=document_identification,
            identification=identification,
            diia_id=diia_id,
            custom_full_name=custom_full_name,
            custom_full_address=custom_full_address,
            delivery_types=delivery_types,
            offer_request_type=offer_request_type,
        )

    def update_branch(self, branch: Branch) -> Branch:
        """Update existing branch.

        Args:
            branch: Updated branch instance.

        Returns:
            Updated branch.

        Raises:
            DiiaClientException
        """
        return self.branch_service.update_branch(branch)

    def get_offers(
        self, *, branch_id: str, skip: Optional[int] = None, limit: Optional[int] = None
    ) -> OfferList:
        """Get offers list on the branch.

        There may be a lots of offers on one branch.
        So it's recommended to limiting requested offers count.

        Args:
            branch_id: Branch ID.
            skip: Number of offers to be skipped.
            limit: Max number of offers in response.

        Raises:
            DiiaClientException
        """
        return self.offer_service.get_offers(
            branch_id=branch_id, skip=skip, limit=limit
        )

    def create_offer(
        self,
        *,
        branch_id: str,
        name: str,
        sharing: Optional[List[DocumentType]] = None,
        diia_id: Optional[List[DiiaIDAction]] = None,
        return_link: Optional[str] = None,
    ) -> Offer:
        """Create new offer on the branch.

        Args:
            branch_id: Branch ID.
            name: Offer name.
            sharing: List of requested documents.
            diia_id: List of Diia ID actions.
            return_link: Link where the customer should be redirected
              after documents sharing confirmation

        Returns:
            Created offer.

        Raises:
            DiiaClientException
        """
        return self.offer_service.create_offer(
            branch_id=branch_id,
            name=name,
            return_link=return_link,
            sharing=sharing,
            diia_id=diia_id,
        )

    def delete_offer(self, branch_id: str, offer_id: str) -> None:
        """Delete offer.

        Args:
            branch_id: Branch ID where the offer was created.
            offer_id: Offer ID.

        Raises:
            DiiaClientException
        """
        return self.offer_service.delete_offer(branch_id=branch_id, offer_id=offer_id)

    def get_deep_link(self, *, branch_id: str, offer_id: str, request_id: str) -> str:
        """Get deep link to start document sharing procedure using online scheme.

        Args:
            branch_id: Branch ID.
            offer_id: Offer ID, Offer with sharing scopes.
            request_id: Unique request id to identify document sharing action;
              it will be sent in http-header with document pack.

        Returns:
            URL, the deep link that should be opened on mobile device
              where Diia application is installed.

        Raises:
            DiiaClientException
        """
        return self.sharing_service.get_deep_link(
            branch_id=branch_id, offer_id=offer_id, request_id=request_id
        )

    def get_sign_deep_link(
        self,
        *,
        branch_id: str,
        offer_id: str,
        request_id: str,
        files: List[File],
    ) -> str:
        """Get deep link for sign files.

        Args:
            branch_id: Branch ID.
            offer_id: Offer ID, offer with `diia_id:hashedFilesSigning` scopes.
            request_id: Unique request id to identify sign action;
              it will be sent in http-header with signatures pack.
            files: List of files for sign.

        Returns:
            URL, the deep link that should be opened on mobile device
              where Diia application is installed.

        Raises:
            DiiaClientException
        """

        return self.sign_service.get_sign_deep_link(
            branch_id=branch_id,
            offer_id=offer_id,
            request_id=request_id,
            files=files,
        )

    def get_auth_deep_link(
        self,
        *,
        branch_id: str,
        offer_id: str,
        request_id: str,
        return_link: Optional[str] = None,
    ) -> AuthDeepLink:
        """Get authorization deep link.

        Args:
            branch_id: Branch ID.
            offer_id: Offer ID, offer with `diia_id:auth` scopes.
            request_id: Unique request id to identify document sharing action;
              hash from request_id will be sent in http-header.
            return_link: Link where the customer should be redirected after authorization

        Returns:
            AuthDeepLink instance.

        Raises:
            DiiaClientException
        """

        return self.sign_service.get_auth_deep_link(
            branch_id=branch_id,
            offer_id=offer_id,
            request_id=request_id,
            return_link=return_link,
        )

    def validate_document_by_barcode(self, *, branch_id: str, barcode: str) -> bool:
        """Validate document by barcode (on the back-side of document).

        Args:
            branch_id: Branch ID.
            barcode: Barcode.

        Returns:
            Sign of document validity.

        Raises:
            DiiaClientException
        """
        return self.validation_service.validate_document_by_barcode(
            branch_id=branch_id, barcode=barcode
        )

    def request_document_by_barcode(
        self, *, branch_id: str, barcode: str, request_id: str
    ) -> bool:
        """Initiate document sharing procedure using document barcode.

        Args:
            branch_id: Branch ID.
            barcode: Barcode.
            request_id: Unique request id to identify document sharing action;
              it will be sent in http-header with document pack.

        Returns:
            Sign of successful request.

        Raises:
            DiiaClientException
        """
        return self.sharing_service.request_document_by_barcode(
            branch_id=branch_id, barcode=barcode, request_id=request_id
        )

    def request_document_by_qrcode(
        self, *, branch_id: str, qrcode: str, request_id: str
    ) -> bool:
        """Initiate document sharing procedure using document QR code.

        Args:
            branch_id: Branch ID.
            qrcode: QR code data.
            request_id: Unique request id to identify document sharing action;
              it will be sent in http-header with document pack

        Returns:
            Sign of successful request.

        Raises:
            DiiaClientException
        """
        return self.sharing_service.request_document_by_qrcode(
            branch_id=branch_id, qrcode=qrcode, request_id=request_id
        )

    def decode_document_package(
        self,
        *,
        headers: StrDict,
        encoded_files: List[EncodedFile],
        encoded_json_data: str,
    ) -> DocumentPackage:
        """Unpacking the documents pack received from Diia, check signatures and decipher documents.

        Args:
            headers: All http-headers from the request from Diia application.
            encoded_files:
              List of EncodedFile based on multipart-body from Diia application request.
            encoded_json_data: Encoded json metadata

        Returns:
            A collection of received documents in PDF format and it's data in json format.

        Raises:
            DiiaClientException
        """
        return self.document_service.process_document_package(
            headers=headers,
            encoded_files=encoded_files,
            encoded_json_data=encoded_json_data,
        )

    def decode_signature_package(
        self,
        *,
        headers: StrDict,
        encode_data: str,
    ) -> SignaturePackage:
        """Unpacking signed items received from Diia.

        Args:
            headers: All http-headers from the request from Diia application.
            encode_data: Base64 encodeData from Diia request.

        Returns:
            A collection of received signatures.

        Raises:
            DiiaClientException
        """
        return self.sign_service.decode_signature_package(
            headers=headers,
            encode_data=encode_data,
        )
