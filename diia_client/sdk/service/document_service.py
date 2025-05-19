import base64
import copy
import json
from typing import List

from diia_client.constants import REQUEST_ID_HEADER
from diia_client.crypto.base_service import AbstractCryptoService
from diia_client.enums import DocumentType
from diia_client.sdk.model import DecodedFile, DocumentPackage, EncodedFile, Metadata
from diia_client.types import DataDict, StrDict
from diia_client.utils import get_headers_value


def normalize_meta(meta: DataDict) -> DataDict:
    """Normalize meta to a common structure.

    Sharing by barcode and deeplink has a different metadata structure:
    by barcode:  "data":{"foreign-passport":{"taxpayerNumber"..
    by deeplink: "data":{"foreign-passport":[{"taxpayerNumber"..

    Returns:
        Metadata dict normalized to deeplink-like structure.
    """

    _meta = copy.deepcopy(meta)
    for doc_type in DocumentType:
        field = doc_type.value
        field_data = _meta["data"].get(field)
        if field_data and isinstance(field_data, dict):
            _meta["data"][field] = [field_data]
    return _meta


class DocumentService:
    def __init__(self, crypto_service: AbstractCryptoService) -> None:
        self.crypto_service = crypto_service

    def process_document_package(
        self,
        *,
        headers: StrDict,
        encoded_files: List[EncodedFile],
        encoded_json_data: str,
    ) -> DocumentPackage:
        request_id = get_headers_value(headers, REQUEST_ID_HEADER)

        decoded_files = []
        for file in encoded_files:
            body = self.crypto_service.decrypt(encrypted_data=file.data, signature=None)
            filename = file.filename.rstrip(".p7s.p7e")
            decoded_files.append(
                DecodedFile(filename=filename, data=base64.b64decode(body))
            )

        meta_b64 = self.crypto_service.decrypt(encoded_json_data, signature=None)
        meta = json.loads(base64.b64decode(meta_b64))
        metadata = Metadata(**normalize_meta(meta))

        return DocumentPackage(
            request_id=request_id,
            files=decoded_files,
            data=metadata,
        )
