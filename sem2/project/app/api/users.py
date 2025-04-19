from fastapi import APIRouter

from app.core.auth import CurrentUser
from app.schemas.users import User

router = APIRouter(tags=['users'])


@router.get('/users/me', response_model=User)
async def me(
        current_user: CurrentUser
):
    return current_user
