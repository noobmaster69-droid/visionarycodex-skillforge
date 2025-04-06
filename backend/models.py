# skillforge/backend/models.py
from sqlalchemy import create_engine, Column, Integer, String, Float, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    job_title = Column(String)
    job_description = Column(String)
    learning_paths = relationship("LearningPath", back_populates="user")
    progress = relationship("Progress", back_populates="user")

class LearningPath(Base):
    __tablename__ = "learning_paths"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    path_data = Column(String)
    user = relationship("User", back_populates="learning_paths")
    contents = relationship("Content", back_populates="learning_path")

class Progress(Base):
    __tablename__ = "progress"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    progress_value = Column(Float)
    user = relationship("User", back_populates="progress")

class Content(Base):
    __tablename__ = "contents"
    id = Column(Integer, primary_key=True, index=True)
    learning_path_id = Column(Integer, ForeignKey("learning_paths.id"))
    topic = Column(String)
    content_text = Column(String)
    media_url = Column(String, nullable=True)
    learning_path = relationship("LearningPath", back_populates="contents")

class Courses(Base):
    __tablename__ = "courses"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    description = Column(String)
    keywords = Column(String, nullable=True)
    content_type = Column(String)