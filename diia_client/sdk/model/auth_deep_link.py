from dataclasses import dataclass


@dataclass
class AuthDeepLink:
    deep_link: str
    request_id: str
    request_id_hash: str
