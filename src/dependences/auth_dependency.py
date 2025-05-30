from typing import Annotated
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from src.configurations.database import get_db
from src.schemas.auth_schema import Token, UserFullResponse
from src.repositories.auth_repo import AuthRepository
from src.utils.auth_util import get_payload


oauth2_schema = OAuth2PasswordBearer(tokenUrl="/auth/login")

def get_current_user_with_db(
    token: Annotated[Token, Depends(oauth2_schema)],
    db: Session = Depends(get_db)
) -> tuple[UserFullResponse, Session]:
    
    payload = get_payload(token)
    email: str = payload.get("sub")
    if email is None:
        pass
    auth_repo = AuthRepository(db)
    user = auth_repo.get_user_by_email(email)
    if not user:
        pass
    return (user, db)