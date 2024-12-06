from fastapi import HTTPException
from sqlalchemy.orm import Session
from ..models.research import Research
from ..schemas.researches import ResearchCreate, ResearchUpdate, ResearchCreateList


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
        description=request.description,
        cost=request.cost,
        duration_in_days=request.duration_in_days,
        category=request.category,
        is_published=request.is_published,
        creator_id=user.id,
    )
    db.add(new_research)
    db.commit()
    db.refresh(new_research)
    return new_research


def update(request: ResearchUpdate, db: Session, research: Research):
    research.title = request.title
    research.description = request.description
    research.cost = request.cost
    research.duration_in_days = request.duration_in_days
    research.category = request.category
    research.is_published = request.is_published
    db.commit()
    db.refresh(research)
    return research


def delete(db: Session, research: Research):
    db.delete(research)
    db.commit()


def create_multiple(request: ResearchCreateList, db: Session, user):
    created_researches = []
    for research_data in request.researches:
        new_research = Research(
            title=research_data.title,
            description=research_data.description,
            cost=research_data.cost,
            duration_in_days=research_data.duration_in_days,
            category=research_data.category,
            is_published=research_data.is_published,
            creator_id=user.id,
        )
        db.add(new_research)
        db.commit()
        db.refresh(new_research)
        created_researches.append(new_research)
    return created_researches


def get_all_paginated(db: Session, limit: int, offset: int):
    return db.query(Research).offset(offset).limit(limit).all()


def is_creator(research: Research, user):
    return research.creator_id == user.id
