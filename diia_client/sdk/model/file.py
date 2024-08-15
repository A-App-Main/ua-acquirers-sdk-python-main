from dataclasses import dataclass


@dataclass
class File:
    filename: str
    data: bytes
