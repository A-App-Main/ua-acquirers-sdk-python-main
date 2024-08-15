from typing import List, Optional

from diia_client.enums import DiiaIDAction, DocumentType
from diia_client.models import BaseModel


class BranchScopes(BaseModel):
    sharing: Optional[List[DocumentType]]
    document_identification: Optional[List[DocumentType]]
    identification: Optional[List[str]]
    diia_id: Optional[List[DiiaIDAction]]
