from typing import List, Optional, Sequence

from diia_client.enums import DiiaIDAction, DocumentType
from diia_client.sdk.remote.model import Branch, BranchList, BranchScopes
from diia_client.sdk.service.base_service import BaseService


class BranchService(BaseService):
    def get_branches(
        self, *, skip: Optional[int] = None, limit: Optional[int] = None
    ) -> BranchList:
        return self.diia_api.get_branches(skip=skip, limit=limit)

    def get_branch(self, branch_id: str) -> Branch:
        return self.diia_api.get_branch_by_id(branch_id)

    def delete_branch(self, branch_id: str) -> None:
        return self.diia_api.delete_branch_by_id(branch_id)

    def create_branch(
        self,
        name: str,
        email: str,
        region: str,
        district: str,
        location: str,
        street: str,
        house: str,
        sharing: Optional[List[DocumentType]] = None,
        document_identification: Optional[List[DocumentType]] = None,
        diia_id: Optional[List[DiiaIDAction]] = None,
        custom_full_name: Optional[str] = None,
        custom_full_address: Optional[str] = None,
        identification: Optional[List[str]] = None,
        delivery_types: Sequence[str] = ("api",),
        offer_request_type: str = "dynamic",
    ) -> Branch:
        scopes = BranchScopes(
            sharing=sharing,
            identification=identification,
            document_identification=document_identification,
            diia_id=diia_id,
        )
        branch = Branch(
            name=name,
            email=email,
            region=region,
            district=district,
            location=location,
            street=street,
            house=house,
            custom_full_name=custom_full_name,
            custom_full_address=custom_full_address,
            scopes=scopes,
            delivery_types=list(delivery_types),
            offer_request_type=offer_request_type,
        )
        branch.id = self.diia_api.create_branch(branch)
        return branch

    def update_branch(self, request: Branch) -> Branch:
        return self.diia_api.update_branch(request)
