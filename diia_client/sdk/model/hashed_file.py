from dataclasses import dataclass


@dataclass
class HashedFile:
    filename: str
    filehash: str
