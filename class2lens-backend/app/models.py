from sqlalchemy import Column, Integer, String
from .database import Base

class Student(Base):
    __tablename__ = "students"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    regno = Column(String, unique=True, nullable=False)
    photo = Column(String, nullable=False)  # stored filename
    fake_embedding = Column(String, nullable=False)  # "fake" vector
