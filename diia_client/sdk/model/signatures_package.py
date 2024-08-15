from dataclasses import dataclass
from typing import List

from diia_client.enums import DiiaIDAction


@dataclass
class Signature:
    filename: str
    signature: str


@dataclass
class SignaturePackage:
    request_id: str
    diia_id_action: DiiaIDAction
    signatures: List[Signature]
