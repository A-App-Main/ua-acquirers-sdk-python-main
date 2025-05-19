from abc import ABC, abstractmethod
from typing import Optional


class AbstractCryptoService(ABC):
    @abstractmethod
    def decrypt(self, encrypted_data: str, signature: Optional[str]) -> str:
        pass

    @abstractmethod
    def calc_hash(self, data: str, algorithm: Optional[str]) -> str:
        pass
