from fastapi import status, HTTPException
from sqlalchemy.orm import Session

from ..config import hashing
from ..models.users import User
from ..schemas.users import UserSchema


def create(db, request):
    new_user = User(name=request.name,
                    email=request.email,
                    password=hashing.get_password_hash(request.password))
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


def get_user_or_404(db, id: int):
    user = db.query(User).filter(User.id == id)

    if not user.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"User with the id {id} is not available")

    return user


def get_user_by_email(db, email: str):
    for record in db:
        user = record.query(User).filter(User.email == email)
        if user:
            return user

    return None


def get_all_paginated(db: Session, limit: int, offset: int):
    return db.query(User).offset(offset).limit(limit).all()


def update_user(db: Session, user: User, request: UserSchema):
    user.name = request.name
    user.email = request.email
    user.password = hashing.get_password_hash(request.password)
    db.commit()
    db.refresh(user)
    return user


def delete_user(db: Session, user: User):
    db.delete(user)
    db.commit()


def get_all(db: Session):
    return db.query(User).all()

