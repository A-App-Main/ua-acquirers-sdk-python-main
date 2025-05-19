from typing import List, Optional

from diia_client.exceptions import DiiaClientException
from diia_client.sdk.http.base_client import AbstractHTTPCLient
from diia_client.sdk.model import HashedFile
from diia_client.sdk.remote.model import Branch, BranchList, Offer, OfferList
from diia_client.sdk.service.session_token_service import SessionTokenService
from diia_client.types import DataDict, StrDict


class DiiaApi:
    def __init__(
        self,
        *,
        acquirer_token: str,
        auth_acquirer_token: str,
        diia_host: str,
        http_client: AbstractHTTPCLient,
    ):
        self.session_token_service = SessionTokenService(
            acquirer_token, auth_acquirer_token, diia_host, http_client
        )
        self.diia_host = diia_host
        self.http_client = http_client

    def _prepare_params(
        self, *, skip: Optional[int] = None, limit: Optional[int] = None
    ) -> DataDict:
        params = {}
        if skip is not None:
            params["skip"] = skip
        if limit is not None:
            params["limit"] = limit
        return params

    def _prepare_headers(self, accept: str = "application/json") -> StrDict:
        token = self.session_token_service.get_session_token()
        return {"Accept": accept, "Authorization": f"Bearer {token}"}

    """
    curl -X POST "{diia_host}/api/v2/acquirers/branch" \
    -H "accept: application/json" \
    -H "Authorization: Bearer {session_token}" \
    -H "Content-Type: application/json" \
    -d "{\"customFullName\":\"Повна назва запитувача документа\",
    \"customFullAddress\":\"Повна адреса відділення\",
    \"name\":\"Назва відділення\", \"email\":\"test@email.com\",
    \"region\":\"Київська обл.\", \"district\":\"Києво-Святошинський р-н\",
    \"location\":\"м. Вишневе\", \"street\":\"вул. Київська\",
    \"house\":\"2г\", \"deliveryTypes\": [\"api\"], \"offerRequestType\": \"dynamic\",
    \"scopes\":{\"sharing\":[\"passport\",\"internal-passport\",
    \"foreign-passport\"], \"identification\":[],
    \"documentIdentification\":[\"internal-passport\",\"foreign-passport\"]}}"
    """

    def create_branch(self, branch: Branch) -> str:
        url = f"{self.diia_host}/api/v2/acquirers/branch"
        try:
            result = self.http_client.post(
                url=url,
                json=branch.dict(by_alias=True),
                headers=self._prepare_headers(),
            )
            return result["_id"]
        except Exception as e:
            raise DiiaClientException("Branch creation error", e) from None

    """
    curl -X GET "{diia_host}/api/v2/acquirers/branch/{branch_id}" \
    -H "accept: application/json" \
    -H "Authorization: Bearer {session_token}"
    """

    def get_branch_by_id(self, branch_id: str) -> Branch:
        url = f"{self.diia_host}/api/v2/acquirers/branch/{branch_id}"
        try:
            result = self.http_client.get(url=url, headers=self._prepare_headers())
            return Branch(**result)
        except Exception as e:
            raise DiiaClientException("Get branch error", e) from None

    """
    curl -X DELETE "{diia_host}/api/v2/acquirers/branch/{branch_id}" \
    -H "Accept: *//*" \
    -H "Authorization: Bearer {session_token}" \
    -H "Content-Type: application/json"
    """

    def delete_branch_by_id(self, branch_id: str) -> None:
        url = f"{self.diia_host}/api/v2/acquirers/branch/{branch_id}"
        try:
            self.http_client.delete(
                url=url, headers=self._prepare_headers(accept="*/*")
            )
        except Exception as e:
            raise DiiaClientException("Delete branch error", e) from None

    """
    curl -X GET "{diia_host}/api/v2/acquirers/branches?skip=0&limit=2" \
    -H "accept: application/json" \
    -H "Authorization: Bearer {session_token}"
    """

    def get_branches(
        self, *, skip: Optional[int] = None, limit: Optional[int] = None
    ) -> BranchList:
        url = f"{self.diia_host}/api/v2/acquirers/branches"
        params = self._prepare_params(skip=skip, limit=limit)

        try:
            result = self.http_client.get(
                url=url, params=params, headers=self._prepare_headers()
            )
            return BranchList(**result)
        except Exception as e:
            raise DiiaClientException("Get branches error", e) from None

    """
    curl -X PUT "{diia_host}/api/v2/acquirers/branch/{branch_id}" \
    -H "Accept: application/json" \
    -H "Authorization: Bearer {session_token}" \
    -H "Content-Type: application/json" \
    -d "{\"customFullName\":\"Повна назва запитувача документа\",
    \"customFullAddress\":\"Повна адреса відділення\",
    \"name\":\"Назва відділення\", \"email\":\"test@email.com\",
    \"region\":\"Київська обл.\", \"district\":\"Києво-Святошинський р-н\",
    \"location\":\"м. Вишневе\", \"street\":\"вул. Київська\",
    \"house\":\"2г\", \"deliveryTypes\": [\"api\"], \"offerRequestType\": \"dynamic\",
    \"scopes\":{\"sharing\":[\"passport\",\"internal passport\",
    \"foreign-passport\"], \"identification\":[],
    \"documentIdentification\":[\"internal-passport\",\"foreign passport\"]}}"
    """

    def update_branch(self, branch: Branch) -> Branch:
        url = f"{self.diia_host}/api/v2/acquirers/branch/{branch.id}"
        try:
            result = self.http_client.put(
                url=url,
                json=branch.dict(by_alias=True),
                headers=self._prepare_headers(),
            )
            branch.id = result["_id"]
            return branch
        except Exception as e:
            raise DiiaClientException("Branch updation error", e) from None

    """
    curl -X POST "https://{diia_host}/api/v1/acquirers/branch/{branch_id}/offer" \
    -H  "accept: application/json" \
    -H  "Authorization: Bearer {session_token}" \
    -H  "Content-Type: application/json" \
    -d "{ \"name\": \"Назва послуги\", \"scopes\": { \"sharing\": [\"passport\"] } }"
    """

    def create_offer(self, *, branch_id: str, offer: Offer) -> str:
        url = f"{self.diia_host}/api/v1/acquirers/branch/{branch_id}/offer"
        try:
            result = self.http_client.post(
                url=url,
                json=offer.dict(by_alias=True, exclude_none=True),
                headers=self._prepare_headers(),
            )
            return result["_id"]
        except Exception as e:
            raise DiiaClientException("Offer creation error", e) from None

    """
    curl -X GET "https://{diia_host}/api/v1/acquirers/branch/{branch_id}/offers?skip=0&limit=100" \
    -H  "accept: application/json" \
    -H  "Authorization: Bearer {session_token}"
    """

    def get_offers(
        self, *, branch_id: str, skip: Optional[int] = None, limit: Optional[int] = None
    ) -> OfferList:

        url = f"{self.diia_host}/api/v1/acquirers/branch/{branch_id}/offers"
        params = self._prepare_params(skip=skip, limit=limit)

        try:
            result = self.http_client.get(
                url=url, params=params, headers=self._prepare_headers()
            )
            return OfferList(**result)
        except Exception as e:
            raise DiiaClientException("Get offers error", e) from None

    """
    curl -X DELETE "https://{diia_host}/api/v1/acquirers/branch/{branch_id}/offer/{offer_id}" \
    -H "accept: *//*" \
    -H "Authorization: Bearer {session_token}" \
    -H "Content-Type: application/json"
    """

    def delete_offer(self, *, branch_id: str, offer_id: str) -> None:
        url = f"{self.diia_host}/api/v1/acquirers/branch/{branch_id}/offer/{offer_id}"
        try:
            self.http_client.delete(
                url=url, headers=self._prepare_headers(accept="*/*")
            )
        except Exception as e:
            raise DiiaClientException("Delete offer error", e) from None

    """
    curl -X POST "https://{diia_host}/api/v1/acquirers/document-identification" \
    -H "accept: application/json" \
    -H "Authorization: Bearer {session_token}" \
    -H "Content-Type: application/json" \
    -d "{\"branchId\":\"{branch_id}\",\"barcode\":\"{barcode}\"}"
    """

    def validate_document_by_barcode(self, *, branch_id: str, barcode: str) -> bool:
        url = f"{self.diia_host}/api/v1/acquirers/document-identification"
        try:
            data = {"branchId": branch_id, "barcode": barcode}
            result = self.http_client.post(
                url=url,
                json=data,
                headers=self._prepare_headers(),
            )
            return result["success"]
        except Exception as e:
            raise DiiaClientException("Document validation error", e) from None

    """
    curl -X POST "https://{diia_host}/api/v1/acquirers/document-request" \
    -H  "accept: application/json" \
    -H  "Authorization: Bearer {session_token}" \
    -H  "Content-Type: application/json" \
    -d "{ \"branchId\": \"{branch_id}\", \"barcode\": \"{barcode}\",
    \"requestId\": \"{request_id}\" }"
    """

    def request_document_by_barcode(
        self, *, branch_id: str, barcode: str, request_id: str
    ) -> bool:
        url = f"{self.diia_host}/api/v1/acquirers/document-request"
        try:
            data = {"branchId": branch_id, "barcode": barcode, "requestId": request_id}
            result = self.http_client.post(
                url=url,
                json=data,
                headers=self._prepare_headers(),
            )
            return result["success"]
        except Exception as e:
            raise DiiaClientException("Document request error", e) from None

    """
    curl -X POST "https://{diia_host}/api/v1/acquirers/document-request" \
    -H  "accept: application/json" \
    -H  "Authorization: Bearer {session_token}" \
    -H  "Content-Type: application/json" \
    -d "{ \"branchId\": \"{branch_id}\", \"qrcode\": \"{qrcode}\",
    \"requestId\": \"{request_id}\" }"
    """

    def request_document_by_qrcode(
        self, *, branch_id: str, qrcode: str, request_id: str
    ) -> bool:
        url = f"{self.diia_host}/api/v1/acquirers/document-request"
        try:
            data = {"branchId": branch_id, "qrcode": qrcode, "requestId": request_id}
            result = self.http_client.post(
                url=url,
                json=data,
                headers=self._prepare_headers(),
            )
            return result["success"]
        except Exception as e:
            raise DiiaClientException("Document request error", e) from None

    """
    curl -X POST "https://{diia_host}/api/v2/acquirers/branch/{branch_id}/offer-request/dynamic"
    -H  "accept: application/json" \
    -H  "Authorization: Bearer {session_token}" \
    -H  "Content-Type: application/json" \
    -d "{ \"offerId\": \"{offer_id}\", \"requestId\": \"{request_id}\" }"
    """

    def get_deep_link(
        self,
        *,
        branch_id: str,
        offer_id: str,
        request_id: str,
        return_link: Optional[str] = None,
        hashed_files: Optional[List[HashedFile]] = None,
    ) -> str:
        url = f"{self.diia_host}/api/v2/acquirers/branch/{branch_id}/offer-request/dynamic"
        try:
            data: DataDict = {"offerId": offer_id, "requestId": request_id}

            # auth
            if return_link is not None:
                data["returnLink"] = return_link

            # sign hashes
            if hashed_files is not None:
                data["data"] = {
                    "hashedFilesSigning": {
                        "hashedFiles": [
                            {
                                "fileName": f.filename,
                                "fileHash": f.filehash,
                            }
                            for f in hashed_files
                        ]
                    }
                }

            result = self.http_client.post(
                url=url,
                json=data,
                headers=self._prepare_headers(),
            )
            return result["deeplink"]
        except Exception as e:
            raise DiiaClientException("DeepLink request error", e) from None
