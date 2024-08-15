import base64
import json
import os
from typing import List, Optional

from diia_client.constants import DIIA_ID_ACTION_HEADER, REQUEST_ID_HEADER
from diia_client.crypto.base_service import AbstractCryptoService
from diia_client.enums import DiiaIDAction
from diia_client.sdk.model import (
    AuthDeepLink,
    File,
    HashedFile,
    Signature,
    SignaturePackage,
)
from diia_client.sdk.remote.diia_api import DiiaApi
from diia_client.types import StrDict
from diia_client.utils import get_headers_value_required


class SignService:
    def __init__(
        self, *, diia_api: DiiaApi, crypto_service: AbstractCryptoService
    ) -> None:
        self.diia_api = diia_api
        self.crypto_service = crypto_service

    def _build_signature_filename(self, filename: str) -> str:
        # replace last file extension to .p7s
        # prevent directory traversal
        base = os.path.splitext(os.path.basename(filename))[0]
        return f"{base}.p7s"

    def get_sign_deep_link(
        self,
        branch_id: str,
        offer_id: str,
        request_id: str,
        files: List[File],
    ) -> str:
        hashed_files = [
            HashedFile(
                filename=file.filename,
                filehash=self.crypto_service.calc_hash(
                    base64.b64encode(file.data).decode()
                ),
            )
            for file in files
        ]

        return self.diia_api.get_deep_link(
            branch_id=branch_id,
            offer_id=offer_id,
            request_id=request_id,
            hashed_files=hashed_files,
        )

    def get_auth_deep_link(
        self,
        branch_id: str,
        offer_id: str,
        request_id: str,
        return_link: Optional[str] = None,
    ) -> AuthDeepLink:

        request_id_hash = self.crypto_service.calc_hash(
            base64.b64encode(request_id.encode()).decode()
        )

        deep_link = self.diia_api.get_deep_link(
            branch_id=branch_id,
            offer_id=offer_id,
            request_id=request_id_hash,
            return_link=return_link,
        )

        return AuthDeepLink(
            deep_link=deep_link,
            request_id=request_id,
            request_id_hash=request_id_hash,
        )

    def decode_signature_package(
        self, headers: StrDict, encode_data: str
    ) -> SignaturePackage:

        request_id = get_headers_value_required(headers, REQUEST_ID_HEADER)

        diia_id_action = DiiaIDAction(
            get_headers_value_required(headers, DIIA_ID_ACTION_HEADER)
        )

        request_data_bytes = base64.b64decode(encode_data)
        request_data = json.loads(request_data_bytes.decode())

        if diia_id_action == DiiaIDAction.HASHED_FILES_SIGNING:
            signatures = [
                Signature(
                    filename=self._build_signature_filename(s["name"]),
                    signature=s["signature"],
                )
                for s in request_data["signedItems"]
            ]
        else:
            signatures = [
                # set filename to auth.p7s, because request_data["requestId"]
                # is crypto-hash and not url/filesystem-safe
                # request_data["requestId"] == request_id from headers
                Signature(
                    filename="auth.p7s",
                    signature=request_data["signature"],
                )
            ]

        return SignaturePackage(
            request_id=request_id,
            diia_id_action=diia_id_action,
            signatures=signatures,
        )
