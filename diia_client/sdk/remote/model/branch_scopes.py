from typing import List, Optional

from diia_client.enums import DiiaIDAction, DocumentType
from diia_client.models import BaseModel


class BranchScopes(BaseModel):
    sharing: Optional[List[DocumentType]] = None
    document_identification: Optional[List[DocumentType]] = None
    identification: Optional[List[str]] = None
    diia_id: Optional[List[DiiaIDAction]] = None
