from typing import Optional

from diia_client.exceptions import DiiaClientException
from diia_client.types import StrDict


def get_headers_value(headers: StrDict, key: str) -> Optional[str]:
    return {k.lower(): v for k, v in headers.items()}.get(key)


def get_headers_value_required(headers: StrDict, key: str) -> str:
    value = get_headers_value(headers, key)
    if value is None:
        raise DiiaClientException(f"Header: {key} not exists")
    return value
