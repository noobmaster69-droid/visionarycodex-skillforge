# skillforge/backend/main.py
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional
from backend.services import skill_inference, learning_path, content_gen, pacing, progress, course_search
from backend.database import create_db_and_tables, SessionLocal, User, LearningPath, Progress, Content
from google.cloud import texttospeech
import json
from backend.models import Courses

import logging
from fastapi import FastAPI, HTTPException

app = FastAPI()

logging.basicConfig(level=logging.DEBUG)

create_db_and_tables()

class JobInput(BaseModel):
    job_input: str

class LearningPathResponse(BaseModel):
    path: List[str]

class ContentResponse(BaseModel):
    content: str
    media_url: Optional[str] = None

class ProgressResponse(BaseModel):
    progress: float

class CreateUser(BaseModel):
    job_input: str

class UpdateProgress(BaseModel):
    user_id: int
    new_progress: float

@app.post("/create_user/")
async def create_user(user: CreateUser):
    db = SessionLocal()
    try:
        new_user = User(job_title=user.job_input, job_description=user.job_input)
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        return {"user_id": new_user.id}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error creating user: {e}")
    finally:
        db.close()

@app.post("/infer_skills")
async def infer_skills(job_input: JobInput):
    try:
        skills = infer_skills(job_input.job_input)
        return skills
        # Your logic here using job_input.job_input
        # return {"skills": ["example_skill1", "example_skill2"]}
    except Exception as e:
        logging.error(f"Error processing request: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")

@app.post("/generate_path/", response_model=LearningPathResponse)
async def generate_path(skills: List[str], user_id:int):
    path = learning_path.generate_learning_path(skills)
    db = SessionLocal()
    try:
        new_learning_path = LearningPath(user_id=user_id, path_data=json.dumps(path))
        db.add(new_learning_path)
        db.commit()
        db.refresh(new_learning_path)
        return {"path": path, "learning_path_id": new_learning_path.id}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error creating learning path: {e}")
    finally:
        db.close()

# ... (rest of main.py)