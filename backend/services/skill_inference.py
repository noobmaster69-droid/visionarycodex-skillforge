# skillforge/backend/services/skill_inference.py
from langchain_google_vertexai import VertexAI
from langchain.prompts import PromptTemplate

def infer_skills(job_input: str):
    """
    Infers skills from a single line of job input.

    Args:
        job_input (str): The job title or description as a single string.

    Returns:
        list: A list of inferred skills.
    """
    llm = VertexAI(
        model="gemini-2.0-flash-001",
        project="platinum-scout-456204-j6",
        location="us-central1",
    )
    prompt = PromptTemplate(
        input_variables=["job_input"],
        template="Extract skills from the following job description: {job_input}",
    )
    chain = prompt | llm
    skills_string = chain.invoke({"job_input": job_input})
    skills = [s.strip() for s in skills_string.split(",")]
    return skills