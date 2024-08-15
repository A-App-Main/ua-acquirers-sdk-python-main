from diia_client.sdk.service.base_service import BaseService


class SharingService(BaseService):
    def get_deep_link(self, branch_id: str, offer_id: str, request_id: str) -> str:
        return self.diia_api.get_deep_link(
            branch_id=branch_id, offer_id=offer_id, request_id=request_id
        )

    def request_document_by_barcode(
        self, branch_id: str, barcode: str, request_id: str
    ) -> bool:
        return self.diia_api.request_document_by_barcode(
            branch_id=branch_id,
            barcode=barcode,
            request_id=request_id,
        )

    def request_document_by_qrcode(
        self, branch_id: str, qrcode: str, request_id: str
    ) -> bool:
        return self.diia_api.request_document_by_qrcode(
            branch_id=branch_id,
            qrcode=qrcode,
            request_id=request_id,
        )
