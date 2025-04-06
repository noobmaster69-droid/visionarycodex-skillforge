# skillforge/backend/services/progress.py
from backend.database import SessionLocal, Progress, LearningPath, Content
from backend.models import Progress
import json

def update_progress(user_id: int, new_progress: float):
    """
    Updates the user's progress in the database.

    Args:
        user_id (int): The ID of the user.
        new_progress (float): The new progress value (0.0 to 1.0).
    """
    db = SessionLocal()
    try:
        progress = db.query(Progress).filter(Progress.user_id == user_id).first()
        if progress:
            progress.progress_value = new_progress
        else:
            new_progress_record = Progress(user_id=user_id, progress_value=new_progress)
            db.add(new_progress_record)
        db.commit()
    except Exception as e:
        db.rollback()
        print(f"Error updating progress: {e}")
    finally:
        db.close()

def get_progress(user_id: int):
    """
    Retrieves the user's progress from the database.

    Args:
        user_id (int): The ID of the user.

    Returns:
        float: The user's progress value, or 0.0 if not found.
    """
    db = SessionLocal()
    try:
        progress = db.query(Progress).filter(Progress.user_id == user_id).first()
        if progress:
            return progress.progress_value
        else:
            return 0.0
    except Exception as e:
        print(f"Error getting progress: {e}")
        return 0.0
    finally:
        db.close()

def calculate_progress(user_id: int):
    """
    Calculates the user's progress based on completed content.
    """
    db = SessionLocal()
    try:
        learning_path = db.query(LearningPath).filter(LearningPath.user_id == user_id).first()
        if learning_path:
            content_count = db.query(Content).filter(Content.learning_path_id == learning_path.id).count()
            if content_count == 0:
                return 0.0

            # Example: Assume each content item represents a step in the learning path.
            progress = db.query(Progress).filter(Progress.user_id == user_id).first()
            if progress:
                current_progress = progress.progress_value
            else:
                current_progress = 0.0
            return min(1.0, current_progress) #ensure it does not exceed 1.0.

        else:
            return 0.0
    except Exception as e:
        print(f"Error calculating progress: {e}")
        return 0.0
    finally:
        db.close()