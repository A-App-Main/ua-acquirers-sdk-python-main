import base64
import logging
import uuid
from pathlib import Path
from typing import Dict, List, Optional

from diia_client import Diia, DiiaIDAction, DocumentType, File
from fastapi import APIRouter, Depends, Form, Request, Response, UploadFile
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates

from app.lib.auth import check_basic_auth
from app.lib.utils import create_qr_code_b64, read_file_as_bytes


logger = logging.getLogger(__name__)
templates = Jinja2Templates(directory=Path(__file__).parent.parent / "templates")
router = APIRouter(dependencies=[Depends(check_basic_auth)])


@router.get("/branches", response_class=HTMLResponse)
async def branches_page(
    request: Request, skip: Optional[int] = None, limit: Optional[int] = None
) -> Response:
    diia: Diia = request.app.state.diia
    branches = diia.get_branches(skip=skip, limit=limit)
    return templates.TemplateResponse(
        "branches.jinja2", {"request": request, "branches": branches}
    )


@router.get("/create-branch", response_class=HTMLResponse)
async def create_branch_page(request: Request) -> Response:
    return templates.TemplateResponse(
        "create_branch.jinja2",
        {
            "request": request,
            "document_types_for_sharing": DocumentType.get_types_for_sharing(),
            "document_types_for_identification": DocumentType.get_types_for_identification(),
            "diia_id_types": DiiaIDAction,
        },
    )


@router.post("/create-branch", response_class=RedirectResponse, status_code=302)
async def create_branch(
    request: Request,
    name: str = Form(...),
    email: str = Form(...),
    region: str = Form(...),
    district: str = Form(...),
    location: str = Form(...),
    street: str = Form(...),
    house: str = Form(...),
    sharing: Optional[List[DocumentType]] = Form(None, alias="Sharing"),
    document_identification: Optional[List[DocumentType]] = Form(
        None, alias="DocumentIdentification"
    ),
    diia_id: Optional[List[DiiaIDAction]] = Form(None, alias="DiiaIDAction"),
    custom_full_name: Optional[str] = Form(None, alias="customfullname"),
    custom_full_address: Optional[str] = Form(None, alias="customfulladdress"),
) -> str:
    diia: Diia = request.app.state.diia
    diia.create_branch(
        name=name,
        email=email,
        region=region,
        district=district,
        location=location,
        street=street,
        house=house,
        custom_full_name=custom_full_name,
        custom_full_address=custom_full_address,
        sharing=sharing,
        document_identification=document_identification,
        diia_id=diia_id,
    )
    return request.url_for("branches_page")


@router.get(
    "/branch/{branch_id}/delete",
    response_class=RedirectResponse,
    status_code=302,
)
async def delete_branch(request: Request, branch_id: str) -> str:
    diia: Diia = request.app.state.diia
    diia.delete_branch(branch_id)
    return request.url_for("branches_page")


@router.get("/branch/{branch_id}/offers", response_class=HTMLResponse)
async def offers_page(
    request: Request,
    branch_id: str,
    skip: Optional[int] = None,
    limit: Optional[int] = None,
) -> Response:
    diia: Diia = request.app.state.diia
    offers = diia.get_offers(branch_id=branch_id, skip=skip, limit=limit)
    return templates.TemplateResponse(
        "offers.jinja2", {"request": request, "branch_id": branch_id, "offers": offers}
    )


@router.get(
    "/branch/{branch_id}/create-offer",
    response_class=HTMLResponse,
)
async def create_offer_page(request: Request, branch_id: str) -> Response:
    diia: Diia = request.app.state.diia
    branch = diia.get_branch(branch_id)
    return templates.TemplateResponse(
        "create_offer.jinja2",
        {
            "request": request,
            "branch_id": branch_id,
            "scopes_sharing": branch.scopes.sharing,
            "scopes_diia_id": branch.scopes.diia_id,
        },
    )


@router.post(
    "/branch/{branch_id}/create-offer",
    response_class=RedirectResponse,
    status_code=302,
)
async def create_offer(
    request: Request,
    branch_id: str,
    name: str = Form(...),
    sharing: Optional[List[DocumentType]] = Form(None, alias="OfferScore"),
    diia_id: Optional[List[DiiaIDAction]] = Form(None, alias="DiiaIDAction"),
    return_link: Optional[str] = Form(None, alias="returnLink"),
) -> str:
    diia: Diia = request.app.state.diia
    diia.create_offer(
        branch_id=branch_id,
        name=name,
        sharing=sharing,
        diia_id=diia_id,
        return_link=return_link,
    )
    return request.url_for("offers_page", branch_id=branch_id)


@router.get(
    "/branch/{branch_id}/offer/{offer_id}/delete",
    response_class=RedirectResponse,
    status_code=302,
)
async def delete_offer(request: Request, branch_id: str, offer_id: str) -> str:
    diia: Diia = request.app.state.diia
    diia.delete_offer(branch_id=branch_id, offer_id=offer_id)
    return request.url_for("offers_page", branch_id=branch_id)


@router.get(
    "/branch/{branch_id}/offer/{offer_id}/deeplink",
    response_class=HTMLResponse,
)
async def share_deeplink(request: Request, branch_id: str, offer_id: str) -> Response:
    diia: Diia = request.app.state.diia
    request_id = str(uuid.uuid4())
    deep_link = diia.get_deep_link(
        branch_id=branch_id,
        offer_id=offer_id,
        request_id=request_id,
    )
    qr_base64 = create_qr_code_b64(deep_link)

    return templates.TemplateResponse(
        "deeplink.jinja2",
        {
            "request": request,
            "deeplink": deep_link,
            "download_url": request.url_for(
                "download-documents", request_id=request_id
            ),
            "qr_base64": qr_base64,
            "request_id": request_id,
        },
    )


@router.get(
    "/branch/{branch_id}/share-barcode",
    name="share-barcode-page",
    response_class=HTMLResponse,
)
@router.get(
    "/branch/{branch_id}/validate-barcode",
    name="validate-barcode-page",
    response_class=HTMLResponse,
)
async def request_document_by_barcode_page(
    request: Request, branch_id: str
) -> Response:
    return templates.TemplateResponse(
        "barcode.jinja2", {"request": request, "branch_id": branch_id}
    )


@router.post(
    "/branch/{branch_id}/share-barcode",
    response_model=Dict[str, str],
)
async def request_document_by_barcode(
    request: Request, branch_id: str, barcode: str = Form(...)
) -> Dict[str, str]:
    diia: Diia = request.app.state.diia
    request_id = str(uuid.uuid4())
    ok = diia.request_document_by_barcode(
        branch_id=branch_id,
        barcode=barcode,
        request_id=request_id,
    )
    return {"requested": str(ok), "request_id": request_id}


@router.post(
    "/branch/{branch_id}/validate-barcode",
    response_model=Dict[str, bool],
)
async def validate_document_by_barcode(
    request: Request, branch_id: str, barcode: str = Form(...)
) -> Dict[str, bool]:
    diia: Diia = request.app.state.diia
    is_valid = diia.validate_document_by_barcode(
        branch_id=branch_id,
        barcode=barcode,
    )
    return {"is_valid": is_valid}


@router.get(
    "/branch/{branch_id}/offer/{offer_id}/sign-deeplink",
    response_class=HTMLResponse,
)
async def sign_deeplink_page(
    request: Request, branch_id: str, offer_id: str
) -> Response:
    return templates.TemplateResponse(
        "sign_documents.jinja2",
        {"request": request, "branch_id": branch_id, "offer_id": offer_id},
    )


@router.post(
    "/branch/{branch_id}/offer/{offer_id}/sign-deeplink",
    response_class=HTMLResponse,
)
async def sign_deeplink(
    request: Request,
    branch_id: str,
    offer_id: str,
    file: UploadFile,
) -> Response:
    diia: Diia = request.app.state.diia
    request_id = str(uuid.uuid4())

    file_data = await read_file_as_bytes(file)

    deep_link = diia.get_sign_deep_link(
        branch_id=branch_id,
        offer_id=offer_id,
        request_id=request_id,
        files=[File(filename=file.filename, data=file_data)],
    )
    qr_base64 = create_qr_code_b64(deep_link)

    request_id_b64 = base64.urlsafe_b64encode(request_id.encode()).decode()

    return templates.TemplateResponse(
        "deeplink.jinja2",
        {
            "request": request,
            "deeplink": deep_link,
            "download_url": request.url_for(
                "download-signatures", request_id_b64=request_id_b64
            ),
            "qr_base64": qr_base64,
            "request_id": request_id,
        },
    )


@router.get(
    "/branch/{branch_id}/offer/{offer_id}/auth-deeplink",
    response_class=HTMLResponse,
)
async def auth_deeplink(request: Request, branch_id: str, offer_id: str) -> Response:
    diia: Diia = request.app.state.diia
    request_id = str(uuid.uuid4())
    auth_deep_link = diia.get_auth_deep_link(
        branch_id=branch_id, offer_id=offer_id, request_id=request_id
    )
    qr_base64 = create_qr_code_b64(auth_deep_link.deep_link)

    request_id_hash_b64 = base64.urlsafe_b64encode(
        auth_deep_link.request_id_hash.encode()
    ).decode()

    return templates.TemplateResponse(
        "deeplink.jinja2",
        {
            "request": request,
            "deeplink": auth_deep_link.deep_link,
            "download_url": request.url_for(
                "download-signatures", request_id_b64=request_id_hash_b64
            ),
            "qr_base64": qr_base64,
            "request_id": request_id,
        },
    )
