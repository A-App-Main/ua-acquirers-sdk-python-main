from dataclasses import dataclass


@dataclass
class EncodedFile:
    filename: str
    data: str
