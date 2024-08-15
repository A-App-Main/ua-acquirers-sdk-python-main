from abc import ABC, abstractmethod


class AbstractCryptoService(ABC):
    @abstractmethod
    def decrypt(self, encrypted_data: str) -> str:
        ...

    @abstractmethod
    def calc_hash(self, data: str) -> str:
        ...
