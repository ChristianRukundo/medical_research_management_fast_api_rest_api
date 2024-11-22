from fastapi import Response, status, HTTPException

from ..models.research import Research


def get_all(db):
    researches = db.query(Research).all()
    return researches


def get_research_or_404(db, id: int):
    research = db.query(Research).filter(Research.id == id)
    if not research.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Research with the id {id} is not available")
    return research


def create(request, db, user):
    new_research = Research(title=request.title, body=request.body, creator_id=user.id)
    db.add(new_research)
    db.commit()
    db.refresh(new_research)
    return new_research


def update(request, db, research):
    research.update(request.dict(), synchronize_session=False)
    db.commit()
    return {
        "detail": "Successfully updated"
    }


def delete(db, research):
    research.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


def is_creator(research, user):
    if research.first().creator_id != user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f"You don't have permission to edit research with the id {id}")
    return True

