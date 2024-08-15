from abc import ABC, abstractmethod
from typing import Optional

from diia_client.types import DataDict, StrDict


DEFAULT_TIMEOUT = 15


class AbstractHTTPCLient(ABC):
    @abstractmethod
    def get(
        self,
        url: str,
        params: Optional[DataDict] = None,
        headers: Optional[StrDict] = None,
        timeout: float = DEFAULT_TIMEOUT,
    ) -> DataDict:
        ...

    @abstractmethod
    def post(
        self,
        url: str,
        json: DataDict,
        params: Optional[DataDict] = None,
        headers: Optional[StrDict] = None,
        timeout: float = DEFAULT_TIMEOUT,
    ) -> DataDict:
        ...

    @abstractmethod
    def put(
        self,
        url: str,
        json: DataDict,
        params: Optional[DataDict] = None,
        headers: Optional[StrDict] = None,
        timeout: float = DEFAULT_TIMEOUT,
    ) -> DataDict:
        ...

    @abstractmethod
    def delete(
        self,
        url: str,
        params: Optional[DataDict] = None,
        headers: Optional[StrDict] = None,
        timeout: float = DEFAULT_TIMEOUT,
    ) -> None:
        ...
