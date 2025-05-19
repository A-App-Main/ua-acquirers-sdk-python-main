from typing import Optional

from diia_client.models import BaseModel


class Document(BaseModel):
    serie: str
    number: str
    department: str
    issue_date: str


class Child(BaseModel):
    last_name: str
    first_name: str
    middle_name: str
    birth_date: str
    birth_place: str
    current_registration_place_ua: Optional[str] = None
    citizenship: Optional[str] = None


class Parent(BaseModel):
    full_name: str
    citizenship: Optional[str] = None


class Parents(BaseModel):
    father: Parent
    mother: Parent


class Act(BaseModel):
    name: str
    registration_place: str


class BirthCertificate(BaseModel):
    id: str
    document: Document
    child: Child
    parents: Parents
    act: Act
