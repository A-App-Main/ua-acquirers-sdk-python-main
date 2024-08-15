from diia_client.models import BaseModel


class VehicleLicense(BaseModel):
    license_plate: str
    doc_number: str
    brand: str
    model: str
    vin: str
    color: str
    kind_body: str
    make_year: str
    total_weight: str
    own_weight: str
    capacity: str
    fuel: str
    rank_category: str
    seats_number: str
    standing_number: str
    date_first_reg: str
    date_reg: str
    owner_type: str
    last_name_ua: str
    first_name_ua: str
    middle_name_ua: str
    birthday: str
    address: str
