# skillforge/backend/database.py
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from backend.models import Base, User, LearningPath, Progress, Content, Courses

DATABASE_URL = "postgresql://postgres:root@localhost:5432/skillforge"  # Replace with your credentials

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def create_db_and_tables():
    try:
        connection = engine.connect()
        table_check_query = text("""
            SELECT EXISTS (SELECT FROM pg_tables WHERE schemaname = 'public' AND tablename = 'users');
        """)
        result = connection.execute(table_check_query).scalar()

        if not result:
            create_tables_query = text("""
                CREATE TABLE users (
                    id SERIAL PRIMARY KEY,
                    job_title TEXT,
                    job_description TEXT
                );

                CREATE TABLE learning_paths (
                    id SERIAL PRIMARY KEY,
                    user_id INTEGER REFERENCES users(id),
                    path_data TEXT
                );

                CREATE TABLE progress (
                    id SERIAL PRIMARY KEY,
                    user_id INTEGER REFERENCES users(id),
                    progress_value REAL
                );

                CREATE TABLE contents (
                    id SERIAL PRIMARY KEY,
                    learning_path_id INTEGER REFERENCES learning_paths(id),
                    topic TEXT,
                    content_text TEXT,
                    media_url TEXT
                );
                CREATE TABLE courses (
                    id SERIAL PRIMARY KEY,
                    title TEXT,
                    description TEXT,
                    keywords TEXT,
                    content_type TEXT
                );
            """)

            connection.execute(create_tables_query)
            connection.commit()
        connection.close()
    except Exception as e:
        print(f"An error occurred during database setup: {e}")