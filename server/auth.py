from typing import Annotated

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from google.auth.transport import requests as grequests
from google.oauth2 import id_token
from pydantic import BaseModel

from server.config import Config
from server.logs import get_logger

logger = get_logger(__name__)

GOOGLE_CLIENT_ID = Config.oauth_client_id
GOOGLE_CLIENT_SECRET = Config.oauth_client_secret


class AuthUser(BaseModel):
    sub: str
    email: str
    name: str
    aud: str


security = HTTPBearer(
    scheme_name="bearer_token",
)


def get_user(
    credentials: Annotated[HTTPAuthorizationCredentials, Depends(security)],
) -> AuthUser:
    token = credentials.credentials
    try:
        # This verifies signature, expiry, issuer, and audience automatically
        raw_id_info = id_token.verify_oauth2_token(token, grequests.Request())  # type: ignore
        user = AuthUser(**raw_id_info)  # type: ignore

        logger.info(f"Authenticated user: {user=}")

        if user.aud != GOOGLE_CLIENT_ID:
            raise ValueError("Token has wrong audience")

        return user
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Invalid or expired token: {e}",
        ) from e
