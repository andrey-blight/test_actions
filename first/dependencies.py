from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from auth.dependencies import get_current_active_user as auth_get_current_active_user
from auth.exceptions import PermissionDenied
from database import get_session
from first.constants import UserRole
from first.exceptions import UserExistWithPhone, UserNotExist, UserOwnerDenied, UserRoleDenied
from first.models import User, UserCreate, UserRead, UserUpdate
from first.services import get_detail_by_id, get_detail_by_email, has_permission


async def user_exist(user: UserCreate, session=Depends(get_session)) -> UserCreate:
    exist_user = await get_detail_by_email(session=session, email=user.email)
    if exist_user:
        raise UserExistWithPhone
    return user


async def user_not_exist(
        user_id: int, session=Depends(get_session),
        current_user=Depends(auth_get_current_active_user)
) -> User:
    if current_user.id != user_id:
        user = await get_detail_by_id(session=session, id=user_id, current_user=current_user)
        if not user:
            raise UserNotExist
    return user_id


async def get_current_user_with_create_permissions(
        user: UserCreate = Depends(user_exist),
        current_user: UserRead = Depends(auth_get_current_active_user)
):
    if not has_permission(current_user.role, user):
        raise UserRoleDenied(user.role)
    return current_user


async def get_current_user_with_update_permissions(
        user_id: int = Depends(user_not_exist),
        current_user: UserRead = Depends(auth_get_current_active_user),
        session: AsyncSession = Depends(get_session)):
    exist_user = await get_detail_by_id(session, user_id, current_user)
    if current_user.id != user_id:
        if not has_permission(current_user.role, exist_user):
            raise UserRoleDenied(exist_user.role)
    return current_user


async def get_current_user_with_delete_permissions(
        user_id: int = Depends(user_not_exist),
        current_user=Depends(auth_get_current_active_user),
        session: AsyncSession = Depends(get_session),
):
    exist_user = await get_detail_by_id(session, user_id, current_user)
    if not has_permission(current_user.role, exist_user):
        raise UserRoleDenied(exist_user.role)
    return current_user
