from datetime import datetime
from fastapi import HTTPException
from sqlalchemy.orm import Session
import models, schemas
from schemas import EmailStatus


def get_user(db: Session, user_id: int):
    return (
        db.query(models.User)
        .filter(
        models.User.user_id == user_id,
                models.User.is_deleted == False
        )
        .first()
    )

def get_user_by_username(db: Session, username: str):
    return (
        db.query(models.User)
        .filter(
        models.User.username == username,
            models.User.is_deleted == False
        )
        .first()
    )

def get_user_by_email(db: Session, email: str):
    return (
        db.query(models.User)
        .filter(
    models.User.email == email,
            models.User.is_deleted == False
        )
        .first()
    )

def get_users(db: Session, skip: int = 0, limit: int = 100):
    return (
        db.query(models.User)
            .filter(models.User.is_deleted == False)
            .offset(skip)
            .limit(limit)
            .all()
            )

def create_user(db: Session, user: schemas.UserCreate):
    if user.username == "":
        raise HTTPException(status_code=400, detail="Username cannot be empty")
    if user.email == "":
        raise HTTPException(status_code=400, detail="Email cannot be empty")
    if user.hashed_password == "":
        raise HTTPException(status_code=400, detail="Password cannot be empty")

    if get_user_by_email(db, user.email) is not None:
        return None
    if get_user_by_username(db, user.username) is not None:
        return None
    try:
        db_user = models.User(**user.dict())
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

def update_user(db: Session, user: schemas.UserUpdate):
    db_user = get_user_by_email(db, user.email)
    if db_user is None or db_user.is_deleted:
        raise HTTPException(status_code=404, detail="User not found")
    if db_user.email_status == EmailStatus.pending_verification or db_user.verified_at is None:
        raise HTTPException(status_code=400, detail="Email is not verified")

    # Check if the new username is unique in database
    if user.username and user.username != db_user.username:
        if get_user_by_username(db, user.username) is not None:
            raise HTTPException(status_code=400, detail="Username is already taken")
        db_user.username = user.username

    # Update other fields of db_user
    for key, value in user.dict(exclude_unset=True).items():
        if value is not None:
            setattr(db_user, key, value)
    try:
        db.commit()
        db.refresh(db_user)
        return db_user
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

def delete_user(db: Session, email: str):
    db_user = get_user_by_email(db, email)
    if db_user is None:
        return None
    db_user.is_deleted = True
    db_user.username = f"deleted{db_user.user_id}+{db_user.username}"
    db_user.email = f"deleted{db_user.user_id}+{db_user.email}"
    try:
        db.commit()
        db.refresh(db_user)
        return db_user
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

def verify_user(db: Session, email: str):
    db_user = get_user_by_email(db, email)
    if db_user is None:
        return None
    db_user.email_status = EmailStatus.verified
    db_user.verified_at = datetime.utcnow()
    try:
        db.commit()
        db.refresh(db_user)
        return db_user
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
