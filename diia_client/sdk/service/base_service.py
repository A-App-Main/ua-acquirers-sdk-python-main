from diia_client.sdk.remote.diia_api import DiiaApi


class BaseService:
    def __init__(self, *, diia_api: DiiaApi):
        self.diia_api = diia_api
