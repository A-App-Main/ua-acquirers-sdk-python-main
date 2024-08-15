from enum import Enum, unique
from typing import List


@unique
class DiiaIDAction(str, Enum):
    AUTH = "auth"
    HASHED_FILES_SIGNING = "hashedFilesSigning"


@unique
class DocumentType(str, Enum):
    # Either citizen passport in ID-Card form or biometric foreign passport.
    # It's a recommended way to obtain a passport when it's type doesn't matter.
    PASSPORT = "passport"

    # Citizen passport in ID-Card form
    INTERNAL_PASSPORT = "internal-passport"

    # Biometric foreign passport or simple foreign passport
    FOREIGN_PASSPORT = "foreign-passport"

    # Taxpayer card
    TAXPAYER_CARD = "taxpayer-card"

    # Internally displaced person certificate
    REFERENCE_INTERNALLY_DISPLACED_PERSON = "reference-internally-displaced-person"

    # Child's birth certificate
    BIRTH_CERTIFICATE = "birth-certificate"

    DRIVER_LICENSE = "driver-license"

    VEHICLE_LICENSE = "vehicle-license"

    @staticmethod
    def get_types_for_sharing() -> List["DocumentType"]:
        return [_type for _type in DocumentType]

    @staticmethod
    def get_types_for_identification() -> List["DocumentType"]:
        return [
            DocumentType.INTERNAL_PASSPORT,
            DocumentType.FOREIGN_PASSPORT,
            DocumentType.TAXPAYER_CARD,
            DocumentType.REFERENCE_INTERNALLY_DISPLACED_PERSON,
            DocumentType.BIRTH_CERTIFICATE,
        ]
