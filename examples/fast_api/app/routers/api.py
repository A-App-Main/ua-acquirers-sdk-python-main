import asyncio
import base64
import io
import logging
import zipfile
from typing import Dict, List, Optional

from diia_client import (
    Diia,
    DocumentPackage,
    DocumentType,
    EncodedFile,
    SignaturePackage,
)
from diia_client.exceptions import DiiaClientException
from diia_client.types import DataDict
from fastapi import APIRouter, BackgroundTasks, Request, Response, UploadFile
from fastapi.responses import StreamingResponse

from app.lib.utils import read_file_as_str


STORE_DOCUMENT_PACKAGE_TIMEOUT = 60

router = APIRouter()
logger = logging.getLogger(__name__)


def log_document_package(document_package: DocumentPackage) -> None:
    data = document_package.data.data

    internal_passport_first_name_ua = None
    foreign_passport_first_name_ua = None
    taxpayer_card_first_name_ua = None

    if data.internal_passport:
        internal_passport_first_name_ua = data.internal_passport[0].first_name_ua
    if data.foreign_passport:
        foreign_passport_first_name_ua = data.foreign_passport[0].first_name_ua
    if data.taxpayer_card:
        taxpayer_card_first_name_ua = data.taxpayer_card[0].first_name_ua

    logger.info(
        "Received DocumentPackage",
        extra={
            "decoded_files": [
                {
                    "filename": file.filename,
                    "len": len(file.data),
                }
                for file in document_package.files
            ],
            "meta_document_types": document_package.data.document_types,
            "internal_passport_first_name": internal_passport_first_name_ua,
            "foreign_passport_first_name": foreign_passport_first_name_ua,
            "taxpayer_card_first_name": taxpayer_card_first_name_ua,
        },
    )


async def remove_stored_data_task(storage: DataDict, request_id: str) -> None:
    await asyncio.sleep(STORE_DOCUMENT_PACKAGE_TIMEOUT)
    storage.pop(request_id, None)


async def get_encode_data(request: Request) -> str:
    # TODO find normal way to parse multipart/mixed in FastAPI
    body = (await request.body()).decode()
    body_parts = body.split("\r\n")
    return max(body_parts)


async def receiver_diia_action(
    request: Request,
    background_tasks: BackgroundTasks,
) -> Dict[str, bool]:
    encode_data = await get_encode_data(request)

    package = None
    diia: Diia = request.app.state.diia
    try:
        package = diia.decode_signature_package(
            headers=dict(request.headers), encode_data=encode_data
        )
        logger.info(
            "Received signatures",
            extra={"signatures": [s.filename for s in package.signatures]},
        )
        request.app.state.signatures_storage[package.request_id] = package
        background_tasks.add_task(
            remove_stored_data_task,
            storage=request.app.state.signatures_storage,
            request_id=package.request_id,
        )
    except DiiaClientException:
        logger.exception("Diia decode_signature_package error")
    return {"success": bool(package)}


async def receiver_shared_documents(
    request: Request,
    background_tasks: BackgroundTasks,
) -> Dict[str, bool]:

    form = await request.form()
    encode_data: str = form["encodeData"]

    # deeplink sharing
    encoded_files: List[EncodedFile] = []
    for doc_type in DocumentType:
        encoded_file: Optional[UploadFile] = form.get(doc_type.value)
        if not encoded_file:
            continue
        encoded_file_data = await read_file_as_str(encoded_file)
        encoded_files.append(
            EncodedFile(
                filename=encoded_file.filename,
                data=encoded_file_data,
            )
        )

    # barcode sharing
    encrypted_file: Optional[UploadFile] = form.get("encryptedFile")
    if encrypted_file:
        encrypted_file_name = form.get("encryptedFileName", "_unexpected_")
        encrypted_file_data = await read_file_as_str(encrypted_file)

        encoded_files.append(
            EncodedFile(filename=encrypted_file_name, data=encrypted_file_data)
        )

    logger.info(
        "Received documents",
        extra={"documents": [ef.filename for ef in encoded_files]},
    )

    document_package = None
    diia: Diia = request.app.state.diia
    try:
        document_package = diia.decode_document_package(
            headers=dict(request.headers),
            encoded_files=encoded_files,
            encoded_json_data=encode_data,
        )
        log_document_package(document_package)

        if document_package.request_id:
            request.app.state.documents_storage[
                document_package.request_id
            ] = document_package
            background_tasks.add_task(
                remove_stored_data_task,
                storage=request.app.state.documents_storage,
                request_id=document_package.request_id,
            )

    except DiiaClientException:
        logger.exception("Diia decode_document_package error")

    return {"success": bool(document_package)}


@router.post("/diia/documents-receiver", response_model=Dict[str, bool])
async def documents_receiver(
    request: Request,
    background_tasks: BackgroundTasks,
) -> Dict[str, bool]:
    if "X-Diia-Id-Action" in request.headers:
        return await receiver_diia_action(request, background_tasks)

    return await receiver_shared_documents(request, background_tasks)


@router.get(
    "/download/{request_id}",
    name="download-documents",
    response_class=StreamingResponse,
)
async def download_documents(
    request: Request,
    request_id: str,
) -> Response:

    storage = request.app.state.documents_storage
    if request_id not in storage:
        return Response(status_code=404, content="NOT FOUND")

    package: DocumentPackage = storage.pop(request_id)

    zip_io = io.BytesIO()
    with zipfile.ZipFile(
        zip_io, mode="w", compression=zipfile.ZIP_DEFLATED
    ) as temp_zip:
        temp_zip.writestr("metadata.json", package.data.json(by_alias=True))

        for file in package.files:
            temp_zip.writestr(file.filename, file.data)

    zip_io.seek(0)
    return StreamingResponse(
        zip_io,
        media_type="application/x-zip-compressed",
        headers={
            "Content-Disposition": f"attachment; filename=diia_{request_id}.zip",
        },
    )


@router.get(
    "/download-signatures/{request_id_b64}",
    name="download-signatures",
    response_class=StreamingResponse,
)
async def download_signatures(
    request: Request,
    request_id_b64: str,
) -> Response:

    request_id = base64.urlsafe_b64decode(request_id_b64).decode()

    storage = request.app.state.signatures_storage
    if request_id not in storage:
        return Response(status_code=404, content="NOT FOUND")

    package: SignaturePackage = storage.pop(request_id)

    zip_io = io.BytesIO()
    with zipfile.ZipFile(
        zip_io, mode="w", compression=zipfile.ZIP_DEFLATED
    ) as temp_zip:
        for signature in package.signatures:
            content = base64.b64decode(signature.signature)
            temp_zip.writestr(signature.filename, content)

    zip_io.seek(0)
    return StreamingResponse(
        zip_io,
        media_type="application/x-zip-compressed",
        headers={
            "Content-Disposition": f"attachment; filename=diia_signatures_{request_id}.zip",
        },
    )
