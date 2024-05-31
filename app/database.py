from sqlalchemy.orm import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

#  URL de conexão com o banco de dados
SQLALCHEMY_DATABASE_URL = "mysql+mysqlconnector://docker:docker@localhost:3319/admin"

# função para retornar a SessionLocal
engine = create_engine(SQLALCHEMY_DATABASE_URL)

def get_session():
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()




Base = declarative_base()




from app.microservices.user_microservice.user_model import User
