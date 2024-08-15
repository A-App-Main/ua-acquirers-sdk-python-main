from diia_client.models import BaseModel


class ForeignPassport(BaseModel):
    taxpayer_number: str
    residence_ua: str
    doc_number: str
    gender_ua: str
    nationality_ua: str
    last_name_ua: str
    first_name_ua: str
    middle_name_ua: str
    birthday: str
    birth_place_ua: str
    issue_date: str
    expiration_date: str
    record_number: str
    department_ua: str
    country_code: str
    gender_en: str
    last_name_en: str
    first_name_en: str
    department_en: str
