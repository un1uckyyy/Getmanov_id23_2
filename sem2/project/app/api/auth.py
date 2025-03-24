from fastapi import APIRouter, HTTPException, status

from ..core.auth import create_access_token, verify_password, get_password_hash
from ..cruds.users import get_user, create_user
from ..schemas.auth import Login, Register
from ..schemas.users import UserWithToken

router = APIRouter()

UNAUTHORIZED_EXCEPTION = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Incorrect username or password",
)


@router.post('/login', response_model=UserWithToken)
async def login(
        credentials: Login,
):
    user = get_user(credentials.email)

    if not user:
        raise UNAUTHORIZED_EXCEPTION
    if not verify_password(credentials.password, user.hashed_password):
        raise UNAUTHORIZED_EXCEPTION

    access_token = create_access_token(
        data={"sub": user.email}
    )

    return UserWithToken(id=user.id, email=user.email, token=access_token)


@router.post('/sign-up', response_model=UserWithToken)
async def sign_up(
        credentials: Register
):
    hashed_password = get_password_hash(credentials.password)

    user = create_user(credentials.email, hashed_password)

    access_token = create_access_token(
        data={"sub": user.email}
    )

    return UserWithToken(id=user.id, email=user.email, token=access_token)
