from typing import List, Optional

from pydantic import Field

from diia_client.models import BaseModel
from diia_client.sdk.remote.model.branch_scopes import BranchScopes


class Branch(BaseModel):
    id: str = Field(default="", alias="_id")

    name: str = Field(..., min_length=1, max_length=32)
    email: str = Field(..., min_length=6, max_length=100)
    region: str = Field(..., min_length=4, max_length=100)
    district: str = Field(..., min_length=4, max_length=100)
    location: str = Field(..., min_length=2, max_length=100)
    street: str = Field(..., min_length=4, max_length=100)
    house: str = Field(..., min_length=1, max_length=20)
    custom_full_name: Optional[str] = Field(..., min_length=1, max_length=100)
    custom_full_address: Optional[str] = Field(..., min_length=1, max_length=200)

    scopes: BranchScopes

    delivery_types: List[str]
    offer_request_type: str
