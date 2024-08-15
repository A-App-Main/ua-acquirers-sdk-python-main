from diia_client.sdk.service.base_service import BaseService


class ValidationService(BaseService):
    def validate_document_by_barcode(self, branch_id: str, barcode: str) -> bool:
        return self.diia_api.validate_document_by_barcode(
            branch_id=branch_id,
            barcode=barcode,
        )
