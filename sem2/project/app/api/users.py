from typing import Annotated

from fastapi import APIRouter, Depends

from ..core.auth import get_current_user
from ..schemas.users import User

router = APIRouter(tags=['users'])


@router.get('/users/me', response_model=User)
async def me(
        current_user: Annotated[User, Depends(get_current_user)],
):
    return current_user
