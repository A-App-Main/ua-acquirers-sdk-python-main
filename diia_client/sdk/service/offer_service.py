from typing import List, Optional

from diia_client.enums import DiiaIDAction, DocumentType
from diia_client.sdk.remote.model import Offer, OfferList, OfferScopes
from diia_client.sdk.service.base_service import BaseService


class OfferService(BaseService):
    def get_offers(
        self, *, branch_id: str, skip: Optional[int] = None, limit: Optional[int] = None
    ) -> OfferList:
        return self.diia_api.get_offers(branch_id=branch_id, skip=skip, limit=limit)

    def create_offer(
        self,
        *,
        branch_id: str,
        name: str,
        sharing: Optional[List[DocumentType]] = None,
        diia_id: Optional[List[DiiaIDAction]] = None,
        return_link: Optional[str] = None,
    ) -> Offer:
        scopes = OfferScopes(sharing=sharing, diia_id=diia_id)
        offer = Offer(name=name, return_link=return_link, scopes=scopes)
        offer.id = self.diia_api.create_offer(branch_id=branch_id, offer=offer)
        return offer

    def delete_offer(self, *, branch_id: str, offer_id: str) -> None:
        return self.diia_api.delete_offer(branch_id=branch_id, offer_id=offer_id)
