from typing import List, Optional

from diia_client.enums import DiiaIDAction, DocumentType
from diia_client.models import BaseModel


class OfferScopes(BaseModel):
    sharing: Optional[List[DocumentType]] = None
    diia_id: Optional[List[DiiaIDAction]] = None

    def can_sign(self) -> bool:
        if not self.diia_id:
            return False
        return DiiaIDAction.HASHED_FILES_SIGNING in self.diia_id

    def can_auth(self) -> bool:
        if not self.diia_id:
            return False
        return DiiaIDAction.AUTH in self.diia_id
