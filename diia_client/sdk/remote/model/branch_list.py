from typing import List

from diia_client.models import BaseModel
from diia_client.sdk.remote.model.branch import Branch


class BranchList(BaseModel):
    total: int
    branches: List[Branch]
