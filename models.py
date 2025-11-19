from sqlalchemy import Column, Integer, String, JSON
from database import Base

class Student(Base):
    __tablename__ = "students"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    regno = Column(String, unique=True, nullable=False)
    photo = Column(String, nullable=False)
    embedding = Column(JSON, nullable=False)  # Stores face embeddings
