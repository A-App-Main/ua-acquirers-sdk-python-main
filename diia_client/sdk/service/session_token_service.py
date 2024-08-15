import time

from diia_client.exceptions import DiiaClientException
from diia_client.sdk.http.base_client import AbstractHTTPCLient


SESSION_TOKEN_TIME_TO_LIVE = 2 * 3600 - 5


class SessionTokenService:
    def __init__(
        self, acquirer_token: str, diia_host: str, http_client: AbstractHTTPCLient
    ):
        self.acquirer_token = acquirer_token
        self.diia_host = diia_host
        self.http_client = http_client
        self.session_token_obtain_time = 0
        self.session_token = ""

    def get_session_token(self) -> str:
        now = int(time.time())

        if (now - self.session_token_obtain_time) >= SESSION_TOKEN_TIME_TO_LIVE:
            self.session_token = self.obtain_session_token()
            self.session_token_obtain_time = now
        return self.session_token

    """
    curl -X GET "https://{diia_host}/api/v1/auth/acquirer/{acquirer_token}"
    -H  "accept: application/json" -H "Authorization: Basic {auth_acquirer_token}"
    """

    def obtain_session_token(self) -> str:
        url = f"{self.diia_host}/api/v1/auth/acquirer/{self.acquirer_token}"
        try:
            result = self.http_client.get(
                url=url,
                headers={
                    "Accept": "application/json",
                    "Authorization": f"Bearer {self.acquirer_token}",
                },
            )
            return result["token"]
        except Exception as e:
            raise DiiaClientException("Authentication error", e)
