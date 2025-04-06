# skillforge/backend/services/pacing.py
from backend.database import SessionLocal, LearningPath, Content
import json

def adjust_pacing(user_id: int, time_per_week: int):
    """
    Adjusts the user's learning path based on the time per week.

    Args:
        user_id (int): The ID of the user.
        time_per_week (int): The time the user wants to dedicate per week (in hours).
    """
    db = SessionLocal()
    try:
        learning_path = db.query(LearningPath).filter(LearningPath.user_id == user_id).first()
        if learning_path:
            path_data = json.loads(learning_path.path_data)
            num_topics = len(path_data)
            if num_topics == 0:
              return

            # Simple pacing logic: Distribute topics evenly over the available time.
            hours_per_topic = time_per_week / num_topics

            # Adjust learning path (example: adding estimated time to each topic)
            adjusted_path = [{"topic": topic, "estimated_hours": hours_per_topic} for topic in path_data]
            learning_path.path_data = json.dumps(adjusted_path)
            db.commit()

            # Example: Adjusting which content is delivered.
            # You would need to add a time estimate to your Content model, or some other way to determine content length.
            # Example:
            # contents = db.query(Content).filter(Content.learning_path_id == learning_path.id).all()
            # for content in contents:
            #    if content.estimated_time > hours_per_topic:
            #        # Do not deliver the content now.
            #        pass

        else:
            print(f"No learning path found for user {user_id}")
    except Exception as e:
        db.rollback()
        print(f"Error adjusting pacing: {e}")
    finally:
        db.close()