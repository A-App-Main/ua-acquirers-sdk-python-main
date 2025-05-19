from typing import List, Optional

from pydantic import Field

from diia_client.enums import DocumentType
from diia_client.models import BaseModel
from diia_client.sdk.model.birth_certificate import BirthCertificate
from diia_client.sdk.model.driver_license import DriverLicense
from diia_client.sdk.model.foreign_passport import ForeignPassport
from diia_client.sdk.model.internal_passport import InternalPassport
from diia_client.sdk.model.reference_internally_displaced_person import (
    ReferenceInternallyDisplacedPerson,
)
from diia_client.sdk.model.taxpayer_card import TaxpayerCard
from diia_client.sdk.model.vehicle_license import VehicleLicense


class Data(BaseModel):
    internal_passport: Optional[List[InternalPassport]] = Field(  # type: ignore[literal-required]
        None, alias=DocumentType.INTERNAL_PASSPORT.value
    )
    foreign_passport: Optional[List[ForeignPassport]] = Field(  # type: ignore[literal-required]
        None, alias=DocumentType.FOREIGN_PASSPORT.value
    )
    taxpayer_card: Optional[List[TaxpayerCard]] = Field(  # type: ignore[literal-required]
        None, alias=DocumentType.TAXPAYER_CARD.value
    )
    reference_internally_displaced_person: Optional[
        List[ReferenceInternallyDisplacedPerson]
    ] = Field(  # type: ignore[literal-required]
        None, alias=DocumentType.REFERENCE_INTERNALLY_DISPLACED_PERSON.value
    )
    birth_certificate: Optional[List[BirthCertificate]] = Field(  # type: ignore[literal-required]
        None, alias=DocumentType.BIRTH_CERTIFICATE.value
    )
    driver_license: Optional[List[DriverLicense]] = Field(  # type: ignore[literal-required]
        None, alias=DocumentType.DRIVER_LICENSE.value
    )
    vehicle_license: Optional[List[VehicleLicense]] = Field(  # type: ignore[literal-required]
        None, alias=DocumentType.VEHICLE_LICENSE.value
    )


class Metadata(BaseModel):
    request_id: Optional[str] = None
    barcode: Optional[str] = None
    document_types: List[str]
    data: Data
