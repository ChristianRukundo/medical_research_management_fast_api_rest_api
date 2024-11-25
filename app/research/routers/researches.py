from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from ..models.research import Research
from ..repository import researches
from ..database import get_db
from ..models.users import User
from ..schemas.researches import ResearchCreate, ResearchUpdate, ResearchResponse

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
def read_researches(db: Session = Depends(get_db)):
    return researches.get_all(db)


@router.get('/{id}', response_model=ResearchResponse)
def read_research(id: int, db: Session = Depends(get_db)):
    research = db.query(Research).filter(Research.id == id).first()
    if not research:
        raise HTTPException(status_code=404, detail="Research not found")
    return research


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
