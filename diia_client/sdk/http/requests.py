from typing import Optional

import requests

from diia_client.sdk.http.base_client import DEFAULT_TIMEOUT, AbstractHTTPCLient
from diia_client.types import DataDict, StrDict


class RequestsHTTPClient(AbstractHTTPCLient):
    """AbstractHTTPCLient implementation based on requests lib."""

    def _raise_for_status(self, r: requests.Response) -> None:
        if 400 <= r.status_code < 500:
            msg = f"{r.status_code} Client Error: {r.reason} for url: {r.url}, json: {r.json()}"
            raise requests.HTTPError(msg, response=r)

        elif 500 <= r.status_code < 600:
            r.raise_for_status()

    def get(
        self,
        url: str,
        params: Optional[DataDict] = None,
        headers: Optional[StrDict] = None,
        timeout: float = DEFAULT_TIMEOUT,
    ) -> DataDict:
        r = requests.get(url=url, params=params, headers=headers, timeout=timeout)
        self._raise_for_status(r)
        return r.json()

    def post(
        self,
        url: str,
        json: DataDict,
        params: Optional[DataDict] = None,
        headers: Optional[StrDict] = None,
        timeout: float = DEFAULT_TIMEOUT,
    ) -> DataDict:
        r = requests.post(
            url=url, params=params, headers=headers, json=json, timeout=timeout
        )
        self._raise_for_status(r)
        return r.json()

    def put(
        self,
        url: str,
        json: DataDict,
        params: Optional[DataDict] = None,
        headers: Optional[StrDict] = None,
        timeout: float = DEFAULT_TIMEOUT,
    ) -> DataDict:
        r = requests.put(
            url=url, params=params, headers=headers, json=json, timeout=timeout
        )
        self._raise_for_status(r)
        return r.json()

    def delete(
        self,
        url: str,
        params: Optional[DataDict] = None,
        headers: Optional[StrDict] = None,
        timeout: float = DEFAULT_TIMEOUT,
    ) -> None:
        r = requests.delete(url=url, params=params, headers=headers, timeout=timeout)
        self._raise_for_status(r)
