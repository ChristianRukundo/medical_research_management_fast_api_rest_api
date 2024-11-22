from typing import List
from fastapi import APIRouter, Depends, status, HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from ..models.research import Research
from ..repository import researches
from ..database import get_db
from ..models.users import User
from ..schemas.researches import ResearchInfoSchema

router = APIRouter(
    prefix="/researches",
    tags=["researches"],
)


@router.post('/create', status_code=status.HTTP_201_CREATED)
def create_research(request: dict,  # Accepting a plain dictionary for simplicity
                user_id: int,
                db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        return JSONResponse(status_code=404, content={"detail": "User not found"})

    research = researches.create(request, db, user)
    return JSONResponse(status_code=201, content={"detail": "Research created successfully", "research": research})


@router.get('/', response_model=List[dict])
def read_researches(db: Session = Depends(get_db)):
    researches_list = researches.get_all(db)
    return JSONResponse(status_code=200, content=[research.to_dict() for research in researches_list])


@router.get('/{id}', response_model=ResearchInfoSchema)
async def read_research(id: int, db: Session = Depends(get_db)):
    research = db.query(Research).filter(Research.id == id).first()
    if not research:
        raise HTTPException(status_code=404, detail="Research not found")

    return JSONResponse(status_code=200, content=research.to_dict())


@router.put('/{id}', status_code=status.HTTP_202_ACCEPTED)
def update_research(id: int, request: dict,
                user_id: int,
                db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        return JSONResponse(status_code=404, content={"detail": "User not found"})

    research = researches.get_research_or_404(db, id)
    if not research:
        return JSONResponse(status_code=404, content={"detail": "Research not found"})

    if researches.is_creator(research, user):
        updated_research = researches.update(request, db, research)
        return JSONResponse(status_code=202, content={"detail": "Research updated successfully", "research": updated_research})
    else:
        return JSONResponse(status_code=403, content={"detail": "You are not authorized to update this research"})


@router.delete('/{id}')
def delete_research(id: int, user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        return JSONResponse(status_code=404, content={"detail": "User not found"})

    research = researches.get_research_or_404(db, id)
    if not research:
        return JSONResponse(status_code=404, content={"detail": "Research not found"})

    if researches.is_creator(research, user):
        researches.delete(db, research)
        return JSONResponse(status_code=200, content={"detail": "Research deleted successfully"})
    else:
        return JSONResponse(status_code=403, content={"detail": "You are not authorized to delete this research"})
