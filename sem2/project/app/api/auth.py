from fastapi import APIRouter, HTTPException, status

from ..core.auth import create_access_token, verify_password, get_password_hash
from ..cruds.users import get_user_by_email, create_user
from ..db.sqlite import DbSession
from ..schemas.auth import Login, Register
from ..schemas.users import UserWithToken

router = APIRouter(tags=["auth"])

UNAUTHORIZED_EXCEPTION = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Incorrect username or password",
)

ALREADY_EXISTS_EXCEPTION = HTTPException(
    status_code=status.HTTP_409_CONFLICT,
    detail="User with that email already exists",
)


@router.post('/login', response_model=UserWithToken)
async def login(
        credentials: Login,
        db: DbSession,
):
    user = get_user_by_email(db, credentials.email)

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
        credentials: Register,
        db: DbSession,
):
    user_exists = get_user_by_email(db, credentials.email)
    if user_exists:
        raise ALREADY_EXISTS_EXCEPTION

    hashed_password = get_password_hash(credentials.password)

    new_user = create_user(db, credentials.email, hashed_password)

    access_token = create_access_token(
        data={"sub": new_user.email}
    )

    return UserWithToken(id=new_user.id, email=new_user.email, token=access_token)
