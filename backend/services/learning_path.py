# skillforge/backend/services/learning_path.py
from langchain_google_vertexai import VertexAI
from langchain.prompts import PromptTemplate

def generate_learning_path(skills: list):
    """
    Generates a learning path based on a list of skills.

    Args:
        skills (list): A list of skills.

    Returns:
        list: A list of learning path topics.
    """
    llm = VertexAI(
        model="gemini-2.0-flash-001",
        project="platinum-scout-456204-j6",
        location="us-central1",
    )
    prompt = PromptTemplate(
        input_variables=["skills"],
        template="Create a learning path for these skills: {skills}",
    )
    chain = prompt | llm
    path_string = chain.invoke({"skills": ", ".join(skills)})
    path = [p.strip() for p in path_string.split("\n")]
    return path