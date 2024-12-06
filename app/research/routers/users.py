from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.params import Query
from sqlalchemy.orm import Session

from ..config import database
from ..repository import users
from ..schemas.users import UserSchema, UserInfoSchema, ShortUserInfoSchema

router = APIRouter(
    prefix="/users",
    tags=["user"],
)


@router.get('/get_all', response_model=List[UserInfoSchema])
def get_all_users(db: Session = Depends(database.get_db)):
    """
    Get all users without pagination.
    """
    return users.get_all(db)


@router.get("/", response_model=List[UserInfoSchema])
def get_all_users(
        db: Session = Depends(database.get_db),
        limit: int = Query(100, ge=1, le=50000),
        offset: int = Query(0, ge=0)
):
    """
    Get all users with pagination.
    :param db:
    :param limit: Number of records to fetch (default: 100, max: 1000).
    :param offset: Offset for the starting record (default: 0).
    """
    return users.get_all_paginated(db, limit=limit, offset=offset)


@router.post('/create', response_model=UserInfoSchema)
def create_user(request: UserSchema, db: Session = Depends(database.get_db)):
    return users.create(db, request)


@router.get('/{id}', response_model=UserInfoSchema)
def read_user(id: int, db: Session = Depends(database.get_db)):
    return users.get_user_or_404(db, id).first()


@router.put('/{id}', response_model=ShortUserInfoSchema, status_code=status.HTTP_202_ACCEPTED)
def update_user(id: int, request: UserSchema, db: Session = Depends(database.get_db)):
    user = users.get_user_or_404(db, id).first()
    if not user:
        raise HTTPException(status_code=404, detail=f"User with id {id} not found")

    updated_user = users.update_user(db, user, request)
    return updated_user


@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_user(id: int, db: Session = Depends(database.get_db)):
    user = users.get_user_or_404(db, id).first()
    if not user:
        raise HTTPException(status_code=404, detail=f"User with id {id} not found")

    users.delete_user(db, user)
    return
