from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.params import Query
from sqlalchemy.orm import Session
from ..repository import researches
from ..config.database import get_db
from ..models.users import User
from ..schemas.researches import ResearchCreate, ResearchUpdate, ResearchResponse, ResearchCreateList

router = APIRouter(
    prefix="/researches",
    tags=["researches"],
)


@router.post('/create', status_code=status.HTTP_201_CREATED, response_model=ResearchResponse)
def create_research(
        request: ResearchCreate,
        user_id: int,
        db: Session = Depends(get_db)
):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    research = researches.create(request, db, user)
    return research


@router.get('/', response_model=List[ResearchResponse])
def read_researches(
        db: Session = Depends(get_db),
        limit: int = Query(100, ge=1, le=50000),
        offset: int = Query(0, ge=0)
):
    """
    Get all research projects with pagination.
    :param db:
    :param limit: Number of records to fetch (default: 100, max: 1000).
    :param offset: Offset for the starting record (default: 0).
    """
    return researches.get_all_paginated(db, limit=limit, offset=offset)


@router.get('/{id}', response_model=ResearchResponse)
def read_research(id: int, db: Session = Depends(get_db)):
    return researches.get_research_or_404(db, id)


@router.put('/{id}', status_code=status.HTTP_202_ACCEPTED, response_model=ResearchResponse)
def update_research(
        id: int,
        request: ResearchUpdate,
        user_id: int,
        db: Session = Depends(get_db)
):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    research = researches.get_research_or_404(db, id)
    if not researches.is_creator(research, user):
        raise HTTPException(status_code=403, detail="You are not authorized to update this research")

    return researches.update(request, db, research)


@router.get('/get_all', response_model=List[ResearchResponse])
def get_all_researches(db: Session = Depends(get_db)):
    """
    Get all research projects without pagination.
    """
    return researches.get_all(db)


@router.post('/create_many', status_code=status.HTTP_201_CREATED, response_model=List[ResearchResponse])
def create_multiple_researches(
        request: ResearchCreateList,
        user_id: int,
        db: Session = Depends(get_db)
):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return researches.create_multiple(request, db, user)


@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_research(id: int, user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    research = researches.get_research_or_404(db, id)
    if not researches.is_creator(research, user):
        raise HTTPException(status_code=403, detail="You are not authorized to delete this research")

    researches.delete(db, research)
    return
