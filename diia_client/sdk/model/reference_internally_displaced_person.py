from diia_client.models import BaseModel


class DocIdentity(BaseModel):
    number: str
    issue_date: str
    department: str


class Address(BaseModel):
    birth: str
    registration: str
    actual: str


class ReferenceInternallyDisplacedPerson(BaseModel):
    doc_type: str
    doc_number: str
    department: str
    last_name: str
    first_name: str
    middle_name: str
    issue_date: str
    birth_date: str
    gender: str
    legal_representative: str
    doc_identity: DocIdentity
    address: Address
