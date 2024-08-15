from dataclasses import dataclass


@dataclass
class DecodedFile:
    filename: str
    data: bytes
