from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import token
from app.database import get_session
from app.microservices.user_microservice.user_repository import UserRepository
from app.microservices.user_microservice.user_schema import User, UserCreate, UserBase, UserLogin
from app.token import Token

router = APIRouter()

@router.post("/login")
def login_user(user: UserLogin, db: Session = Depends(get_session)):
    user_repo = UserRepository(db)
    db_user = user_repo.get_user_by_email(user.email)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")

    if user.password != db_user.password:
        raise HTTPException(status_code=401, detail="Incorrect password")
    token = Token()
    jwt_token = token.generate(db_user.email)
    return {"result": "Login realizado com sucesso", "token":jwt_token}

@router.post("/register", response_model=User)
def register_user(user: UserCreate, db: Session = Depends(get_session)):
    user_repo = UserRepository(db)

    return user_repo.create_user(user)

@router.get("/users/", response_model=list[User])
def get_all_users(db: Session = Depends(get_session)):
    user_repo = UserRepository(db)
    return user_repo.get_all_users()

@router.get("/users/{user_id}", response_model=User)
def get_user(user_id: int, db: Session = Depends(get_session)):
    user_repo = UserRepository(db)
    db_user = user_repo.get_user_by_id(user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

@router.put("/users/{user_id}")
def update_user(user_id: int, user: UserBase, db: Session = Depends(get_session)):
    user_repo = UserRepository(db)
    db_user = user_repo.update_user(user_id, user)

    return db_user

@router.delete("/users/{user_id}", response_model=None)
def delete_user(user_id: int, db: Session = Depends(get_session)):
    try:
        user_repo = UserRepository(db)
        db_user = user_repo.delete_user(user_id)
        return {"message": "User deleted successfully"}
    except Exception as e:
        return {"error": str(e)}