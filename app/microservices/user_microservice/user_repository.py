from sqlalchemy.orm import Session

from app.microservices.user_microservice.user_model import User
from app.microservices.user_microservice.user_schema import UserCreate, UserBase


class UserRepository:
    def __init__(self, db: Session):
        self.db = db

    def create_user(self, user: UserCreate):
        db_user = User(name=user.name, email=user.email, password=user.password)
        self.db.add(db_user)
        self.db.commit()
        self.db.refresh(db_user)
        return db_user

    def get_user_by_email(self, email: str):  # Adicione esta função
        return self.db.query(User).filter(User.email == email).first()



    def get_user_by_id(self, user_id: int):
        return self.db.query(User).filter(User.id == user_id).first()

    def get_all_users(self):
        return self.db.query(User).all()

    def update_user(self, user_id: int, user: UserBase):
        db_user = self.get_user_by_id(user_id)
        db_user.name = user.name
        db_user.email = user.email

        self.db.commit()
        self.db.refresh(db_user)
        return db_user

    def delete_user(self, user_id: int):
        db_user = self.get_user_by_id(user_id)
        self.db.delete(db_user)
        self.db.commit()