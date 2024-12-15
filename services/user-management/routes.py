from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import crud
from schemas import UserCreate, UserUpdate, UserResponse, LoginResponse
from database import get_db

router = APIRouter(
    prefix="/user",
    tags=["user"],
    responses={404: {"description": "Not found"}},
)

@router.get("/")
async def root():
    return {"message": "you are inside User Management Service, it is working fine"}

@router.post("/users/", response_model=UserResponse)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    user = crud.create_user(db=db, user=user)
    if user is None:
        raise HTTPException(status_code=400, detail="Email or Username already registered")
    return user

@router.get("/users/", response_model=list[UserResponse])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = crud.get_users(db, skip=skip, limit=limit)
    return users

@router.get("/users/id/{user_id}", response_model=UserResponse)
def read_user_by_id(user_id: int, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

@router.get("/users/email/login/{email}", response_model=LoginResponse)
def read_user_by_email_for_login(email: str, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, email=email)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

@router.get("/users/email/{email}", response_model=UserResponse)
def read_user_by_email(email: str, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, email=email)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

@router.get("/users/username/{username}", response_model=UserResponse)
def read_user_by_username(username: str, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_username(db, username=username)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

@router.put("/users/", response_model=UserResponse)
def update_user(user: UserUpdate, db: Session = Depends(get_db)):
    db_user = crud.update_user(db, user)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

@router.delete("/users/{email}", response_model=UserResponse)
def delete_user(email: str, db: Session = Depends(get_db)):
    db_user = crud.delete_user(db, email)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

@router.get("/users/verify/{email}", response_model=UserResponse)
def verify_user(email: str, db: Session = Depends(get_db)):
    db_user = crud.verify_user(db, email)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user