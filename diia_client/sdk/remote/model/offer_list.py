from typing import List

from diia_client.models import BaseModel
from diia_client.sdk.remote.model.offer import Offer


class OfferList(BaseModel):
    total: int
    offers: List[Offer]
