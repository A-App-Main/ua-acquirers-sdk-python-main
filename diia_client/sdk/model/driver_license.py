from diia_client.models import BaseModel


class DriverLicense(BaseModel):
    expiration_date: str
    categories: str
    serial_number: str
    last_name_ua: str
    first_name_ua: str
    middle_name_ua: str
    birthday: str
    department: str
