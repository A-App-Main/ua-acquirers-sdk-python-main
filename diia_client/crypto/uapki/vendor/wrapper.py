import ctypes
import json
import os
from sys import platform

from diia_client.types import DataDict


class UAPKI:
    def __loadLib(self, pathToLibsFolder: str) -> None:
        if platform == "linux" or platform == "linux2":
            pathToSo = os.path.join(pathToLibsFolder, "libuapkiNativeWrapper.so")
        elif platform == "win32":
            pathToSo = os.path.join(pathToLibsFolder, "uapkiNativeWrapper.dll")
        elif platform == "darwin":
            pathToSo = os.path.join(pathToLibsFolder, "libuapkiNativeWrapper.dylib")
        else:
            raise OSError("Not supported platform {}".format(platform))

        self.__libSo = ctypes.CDLL(pathToSo)

        # Init
        self.__libSo.Init.argtypes = [
            ctypes.POINTER(ctypes.c_char),
            ctypes.POINTER(ctypes.c_char),
        ]
        self.__libSo.Init.restype = ctypes.c_char_p

        # Unwrap
        self.__libSo.Unwrap.argtypes = [
            ctypes.POINTER(ctypes.c_char),
        ]
        self.__libSo.Unwrap.restype = ctypes.c_char_p

        self.__libSo.DigestGost34311.argtypes = [
            ctypes.POINTER(ctypes.c_char),
        ]
        self.__libSo.DigestGost34311.restype = ctypes.c_char_p

    def __encode_str(self, str: str) -> bytes:
        return str.encode("utf-8")

    def __decode_str(self, bytes: bytes) -> DataDict:
        return json.loads(bytes.decode("utf-8"))

    # pathToConfig - path or config's json
    # pathToLibsFolder - path to folder where all so is stored
    def Init(self, pathToConfig: str, pathToLibsFolder: str) -> DataDict:
        self.__loadLib(pathToLibsFolder)
        return self.__decode_str(
            self.__libSo.Init(
                self.__encode_str(pathToConfig), self.__encode_str(pathToLibsFolder)
            )
        )

    # ret = Unwrap(...)
    # if ret["errorCode"] == 0:
    #   ret["result"]["bytes"] - content info b64
    # if ret["errorCode"] != 0:
    #   ret["method"] -  which method produce error
    #   ret["error"] - error description
    #   ret["result"] == {}
    def Unwrap(self, envelopedDataB64: str) -> DataDict:
        return self.__decode_str(
            self.__libSo.Unwrap(self.__encode_str(envelopedDataB64))
        )

    def DigestGost34311(self, dataB64: str) -> DataDict:
        return self.__decode_str(
            self.__libSo.DigestGost34311(self.__encode_str(dataB64))
        )
