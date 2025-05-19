import logging

from diia_client import Diia
from diia_client.crypto.uapki import UAPKICryptoService
from diia_client.exceptions import DiiaClientException
from diia_client.sdk.http.requests import RequestsHTTPClient
from fastapi import FastAPI, Request, Response
from fastapi.responses import JSONResponse

from app.config import Settings
from app.routers import api, index, views


logger = logging.getLogger(__name__)


def make_diia_client(settings: Settings) -> Diia:

    http_client = RequestsHTTPClient()
    crypto_service = UAPKICryptoService(
        key=settings.key,
        password=settings.password,
        certificate=settings.certificate,
        subject_key_id=settings.subject_key_id,
        diia_certificate=settings.diia_certificate,
        diia_certificate_kep=settings.diia_certificate_kep,
        diia_issuer_certificate=settings.diia_issuer_certificate,
    )

    return Diia(
        acquirer_token=settings.acquirer_token,
        auth_acquirer_token=settings.auth_acquirer_token,
        diia_host=settings.host,
        http_client=http_client,
        crypto_service=crypto_service,
    )


def make_app(settings: Settings) -> FastAPI:
    app = FastAPI(
        debug=settings.debug,
        title=settings.app_title,
        description=settings.app_description,
        version=settings.app_version,
    )
    app.state.settings = settings

    app.state.diia = make_diia_client(settings)

    app.state.documents_storage = {}
    app.state.signatures_storage = {}

    app.include_router(index.router, prefix="", tags=["index"])
    app.include_router(api.router, prefix="/api", tags=["api"])
    app.include_router(views.router, prefix="/views", tags=["views"])

    @app.exception_handler(DiiaClientException)
    async def diia_client_exception_handler(
        request: Request, exc: DiiaClientException
    ) -> Response:
        logger.exception("DiiaClientException")
        return JSONResponse(
            status_code=400,
            content={"error": f"{exc}"},
        )

    logger.info("New app instance was created")

    return app
