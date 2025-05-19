import json
import os
from pathlib import Path
from sys import platform
from typing import Optional

from diia_client.crypto.base_service import AbstractCryptoService
from diia_client.crypto.uapki.vendor.wrapper import UAPKI
from diia_client.exceptions import DiiaClientException
from diia_client.types import DataDict


BASE_DIR = Path(__file__).parent

if platform == "linux" or platform == "linux2":
    VENDOR_DIR = BASE_DIR / "vendor/linux_x86-64"
    os.environ["LD_LIBRARY_PATH"] = str(VENDOR_DIR)
elif platform == "win32":
    VENDOR_DIR = BASE_DIR / "vendor/windows_x86-64"
elif platform == "darwin":
    VENDOR_DIR = BASE_DIR / "vendor/mac_x86-64"
else:
    raise OSError("Not supported platform {}".format(platform))


class UAPKICryptoService(AbstractCryptoService):
    """https://github.com/specinfo-ua/UAPKI"""

    def __init__(
        self,
        key: str,
        password: str,
        certificate: str,
        subject_key_id: str,
        diia_certificate: str,
        diia_certificate_kep: str,
        diia_issuer_certificate: Optional[str] = None,
    ) -> None:
        """UAPKI constructor.

        Requirements:
            Platform: linux_x86-64 | windows_x86-64 | mac_x86-64
            GLIBC_2.34 (use Debian bullseye+ container)
            libcurl

        Args:
            key: Base64 encoded key
            password: Password from key
            certificate: Base64 encoded key's certificate
            subject_key_id: Subject Key Identifier (from certificate)
            diia_certificate: Public Diia certificate (b64 encoded)
            diia_certificate_kep: Public Diia kep certificate (b64 encoded)
            diia_issuer_certificate:
              Optional: Diia cert issuer certificate (b64 encoded)

        Raises:
            DiiaClientException
        """

        self.key = key
        self.password = password
        self.certificate = certificate
        self.subject_key_id = subject_key_id
        self.diia_certificate = diia_certificate
        self.diia_certificate_kep = diia_certificate_kep
        self.diia_issuer_certificate = diia_issuer_certificate

        self._uapki = UAPKI()
        self._init_uapki_config()

    def _init_uapki_config(self) -> None:
        config = self._prepare_config()
        _data = self._uapki.Init(json.dumps(config), f"{VENDOR_DIR}/")
        if _data["errorCode"] != 0:
            raise DiiaClientException(f"Init uapki error: {_data}")

    def _prepare_config(self) -> DataDict:
        trusted_certs = [self.diia_certificate, self.diia_certificate_kep]
        if self.diia_issuer_certificate:
            trusted_certs.append(self.diia_issuer_certificate)

        return {
            "global": {
                "crypto.dstu.env_data_for_diia.storage.b64": self.key,
                "crypto.dstu.env_data_for_diia.storage.password.enc": self.password,
                "crypto.dstu.env_data_for_diia.subjKeyId": self.subject_key_id,
                "crypto.dstu.env_data_for_diia.cert.b64": self.certificate,
                "crypto.trusted_certs_for_diia": trusted_certs,
            },
            "uapki": {
                "cmProviders": {"allowedProviders": [{"lib": "cm-pkcs12"}]},
                "certCache": {
                    "trustedCerts": trusted_certs,
                },
                "offline": False,
                "reportTime": False,
            },
        }

    def _check_result(self, data: DataDict, msg: str) -> None:
        if data["errorCode"] != 0:
            raise DiiaClientException(f"{msg}: {data}")

        if "result" not in data or "bytes" not in data["result"]:
            raise DiiaClientException(
                f"{msg}. Answer doesn't contain field 'result' or 'bytes'"
            )

    def decrypt(self, encrypted_data: str, signature: Optional[str]) -> str:
        """Decrypt data.

        Args:
            encrypted_data: Base64 encoded encrypted data
            signature: Irrelevant in this context

        Returns:
            Base64 encoded decrypted content

        Raises:
            DiiaClientException
        """

        _data: DataDict = self._uapki.Unwrap(encrypted_data)
        self._check_result(_data, "Decryption error")
        return _data["result"]["bytes"]

    def calc_hash(self, data: str, algorithm: Optional[str]) -> str:
        """Hash data.

        Args:
            data: Base64 encoded data.
            algorithm: Irrelevant in this context

        Returns:
            Base64 hash.

        Raises:
            DiiaClientException
        """

        _data: DataDict = self._uapki.DigestGost34311(data)
        self._check_result(_data, "Calculate hash error")
        return _data["result"]["bytes"]
