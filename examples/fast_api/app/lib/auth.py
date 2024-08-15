import logging
import secrets

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials

from app.config import settings


logger = logging.getLogger(__name__)

security = HTTPBasic()


def check_basic_auth(credentials: HTTPBasicCredentials = Depends(security)) -> None:
    correct_username = secrets.compare_digest(
        credentials.username, settings.basic_auth_username
    )
    correct_password = secrets.compare_digest(
        credentials.password, settings.basic_auth_password
    )
    if not (correct_username and correct_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Basic"},
        )
