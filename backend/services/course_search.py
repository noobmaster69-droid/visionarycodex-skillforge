# skillforge/backend/services/course_search.py
from backend.database import SessionLocal
from sqlalchemy import text
from langchain_google_vertexai import VertexAI
from langchain.prompts import PromptTemplate
from backend.models import Courses
from langchain.embeddings import VertexAIEmbeddings
from langchain.vectorstores import FAISS
from langchain.schema import Document
import os

VECTOR_SPACE_PATH = "course_vector_space"

def search_courses(query: str):
    """
    Searches for courses in the database and uses LangChain as a fallback.

    Args:
        query (str): The search query.

    Returns:
        list: A list of search results (dictionaries).
    """
    db = SessionLocal()
    try:
        sql_query = text(
            "SELECT title, description FROM courses WHERE title LIKE :query OR description LIKE :query"
        )
        db_results = db.execute(sql_query, {"query": f"%{query}%"}).fetchall()
        results = [{"title": row.title, "description": row.description} for row in db_results]

        if results:
            return results

        llm = VertexAI(
            model="gemini-2.0-flash-001",
            project="platinum-scout-456204-j6",
            location="us-central1",
        )
        prompt = PromptTemplate(
            input_variables=["query"],
            template="Answer the following question: {query}",
        )
        chain = prompt | llm
        langchain_result = chain.invoke({"query": query})

        new_course = Courses(title=query, description=langchain_result, content_type="search_result")
        db.add(new_course)
        db.commit()

        embeddings = VertexAIEmbeddings()
        if os.path.exists(VECTOR_SPACE_PATH):
            vectorstore = FAISS.load_local(VECTOR_SPACE_PATH, embeddings)
        else:
            vectorstore = FAISS.from_texts([], embeddings)

        vectorstore.add_documents([Document(page_content=langchain_result)])
        vectorstore.save_local(VECTOR_SPACE_PATH)

        return [{"title": query, "description": langchain_result}]

    except Exception as e:
        print(f"Error searching courses: {e}")
        return []
    finally:
        db.close()