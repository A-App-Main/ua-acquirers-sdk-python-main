import pyqrcode
from fastapi import UploadFile


async def read_file_as_str(file: UploadFile) -> str:
    _data = await file.read()
    if isinstance(_data, str):
        return _data
    return _data.decode("utf-8")


async def read_file_as_bytes(file: UploadFile) -> bytes:
    _data = await file.read()
    if isinstance(_data, bytes):
        return _data
    return _data.encode("utf-8")


def create_qr_code_b64(data: str) -> str:
    return pyqrcode.create(data).png_as_base64_str(scale=7)
