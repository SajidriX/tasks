from sqlalchemy import create_engine, Column, Integer, String, Boolean, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy import create_engine, Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import sessionmaker, Session, declarative_base,relationship


SQLALCHEMY_DATABASE_URL = "sqlite:///./task.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


Base = declarative_base()

class Task(Base):
    __tablename__ = "tasks"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    description = Column(String(500))
    priority = Column(Integer, nullable=False)
    user_id = Column(Integer,ForeignKey('users.id'))
    user = relationship("User",back_populates="tasks")

class User(Base):
    __tablename__ = "users"
    id = Column(Integer,primary_key=True)
    name = Column(String(100),nullable=False)
    grade = Column(String(100))
    password = Column(String(100),nullable=False)
    tasks = relationship("Task",back_populates="user",cascade="all, delete orphan")




def init_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()