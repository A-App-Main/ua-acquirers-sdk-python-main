from diia_client.models import BaseModel


class TaxpayerCard(BaseModel):
    creation_date: str
    doc_number: str
    last_name_ua: str
    first_name_ua: str
    middle_name_ua: str
    birthday: str
