""" user admin endpoints """

from typing import List

from fastapi import APIRouter, Body, Depends, HTTPException

from app.core.exceptions import CRUDError
from app.core.security.token import get_current_active_superuser, get_current_active_user
from app.crud.auth import UserCRUD
from app.schema.auth import User, UserCreate, UserList

router = APIRouter()

crud = UserCRUD()

@router.post(
    '/create',
    dependencies=[Depends(get_current_active_superuser)],
    response_model=User,
    response_model_exclude_unset=True
)
async def create_user(user_in: UserCreate):
    """ create a user """

    if not user_in.username and not user_in.email:
        raise HTTPException(status_code=400, detail='username or email is required.')

    try:
        new_user = await crud.create(obj_in=user_in)

    except CRUDError:
        raise HTTPException(
            status_code=400,
            detail='A user with this email or username already exists.'
        )

    return new_user


@router.get(
    '/',
    dependencies=[Depends(get_current_active_user)],
    response_model=List[User],
    response_model_exclude_unset=True
)
async def get_users(skip: int = 0, limit: int = 100):
    """ returns all users """

    user_list = await crud.get_multi(skip=skip, limit=limit)
    return user_list


@router.get('/list', response_model=List[UserList])
async def get_user_list():
    """ returns firstname, lastname and id """

    user_list = await crud.get_multi(limit=0)
    return user_list
