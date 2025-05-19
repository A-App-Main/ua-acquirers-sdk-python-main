from typing import Optional

from pydantic import Field

from diia_client.models import BaseModel
from diia_client.sdk.remote.model.offer_scopes import OfferScopes


class Offer(BaseModel):
    id: str = Field(default="", alias="_id")

    name: str
    return_link: Optional[str] = None
    scopes: OfferScopes
