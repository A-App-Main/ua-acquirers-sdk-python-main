import logging
from pathlib import Path

from fastapi import APIRouter, Depends, Request, Response
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from app.lib.auth import check_basic_auth


logger = logging.getLogger(__name__)
templates = Jinja2Templates(directory=Path(__file__).parent.parent / "templates")
router = APIRouter(dependencies=[Depends(check_basic_auth)])


@router.get("/", name="index", response_class=HTMLResponse)
async def index_page(request: Request) -> Response:
    return templates.TemplateResponse("index.jinja2", {"request": request})
