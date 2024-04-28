# crud.py
from fastapi import HTTPException
from sqlalchemy.orm import Session
from .model import User, Research
from .schemas import UserCreate, ProfessorUpdate, NonProfessorUpdate, ResearchBase, ResearchCreate
from uuid import UUID, uuid4


def update_user(db: Session, user_id: UUID, user_update: dict):
    db_user = db.query(User).filter(User.id == user_id).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")

    # 更新用户信息
    for key, value in user_update.items():
        setattr(db_user, key, value)
    db.commit()
    db.refresh(db_user)
    return db_user


def create_user(db: Session, user_create: UserCreate):
    db_user = User(id=uuid4(), **user_create.dict(exclude_unset=True))
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def delete_user(db: Session, user_id: UUID):
    db_user = db.query(User).filter(User.id == user_id).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    db.delete(db_user)
    db.commit()
    return {"message": "User deleted successfully"}


def get_user(db: Session, user_id: UUID):
    db_user = db.query(User).filter(User.id == user_id).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(User).offset(skip).limit(limit).all()


def create_research(db: Session, research_create: ResearchCreate, professor_id: UUID):
    db_research = Research(
        id=uuid4(),
        research=research_create.research,
        professor_id=professor_id,
        application=research_create.application,
        applied=research_create.applied,
        refused=research_create.refused
    )
    db.add(db_research)
    db.commit()
    db.refresh(db_research)
    return db_research

