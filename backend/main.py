# skillforge/backend/main.py
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional
from services import skill_inference, learning_path, content_gen, pacing, progress, course_search
from database import create_db_and_tables, SessionLocal, User, LearningPath, Progress, Content
from google.cloud import texttospeech
import json
from models import Courses
import os

app = FastAPI()

create_db_and_tables()

SERVICE_ACCOUNT_FILE = "C:\\Users\\Arunachaleshwar\\Desktop\\key.json"
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = SERVICE_ACCOUNT_FILE

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

@app.post("/infer_skills/", response_model=List[str])
async def infer_skills(job_input: JobInput):
    skills = skill_inference.infer_skills(job_input.job_input)
    return skills

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

@app.post("/generate_content/", response_model=ContentResponse)
async def generate_content(topic: str, learning_path_id: int):
    content = content_gen.generate_content(topic)
    media_url = None
    if content:
        media_url = content_gen.generate_audio(content, topic)
    db = SessionLocal()
    try:
        new_content = Content(learning_path_id=learning_path_id, topic=topic, content_text=content, media_url=media_url)
        db.add(new_content)
        db.commit()
        db.refresh(new_content)

        new_course = Courses(title = topic, description = content, content_type = "module")
        db.add(new_course)
        db.commit()

        return {"content": content, "media_url": media_url}

    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error creating content: {e}")
    finally:
        db.close()

@app.post("/adjust_pacing/")
async def adjust_pacing(user_id: int, time_per_week: int):
    pacing.adjust_pacing(user_id, time_per_week)
    return {"message": "Pacing adjusted"}

@app.get("/progress/{user_id}/", response_model=ProgressResponse)
async def get_progress(user_id: int):
    progress_value = progress.get_progress(user_id)
    return {"progress": progress_value}

@app.post("/update_progress/")
async def update_user_progress(progress_update: UpdateProgress):
    progress.update_progress(progress_update.user_id, progress_update.new_progress)
    return {"message": "Progress updated"}

@app.post("/search_courses/")
async def search_courses_api(query: str):
    results = course_search.search_courses(query)
    return {"results": results}