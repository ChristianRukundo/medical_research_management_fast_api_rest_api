from fastapi import Response, status, HTTPException
from sqlalchemy.orm import Session

from ..models.research import Research
from ..schemas.researches import ResearchCreate, ResearchUpdate


def get_all(db: Session):
    return db.query(Research).all()


def get_research_or_404(db: Session, id: int):
    research = db.query(Research).filter(Research.id == id).first()
    if not research:
        raise HTTPException(status_code=404, detail=f"Research with id {id} not found")
    return research


def create(request: ResearchCreate, db: Session, user):
    new_research = Research(
        title=request.title,
        body=request.body,
        creator_id=user.id
    )
    db.add(new_research)
    db.commit()
    db.refresh(new_research)
    return new_research


def update(request: ResearchUpdate, db: Session, research: Research):
    research.title = request.title
    research.body = request.body
    db.commit()
    db.refresh(research)
    return research


def delete(db: Session, research: Research):
    db.delete(research)
    db.commit()


def is_creator(research: Research, user):
    return research.creator_id == user.id