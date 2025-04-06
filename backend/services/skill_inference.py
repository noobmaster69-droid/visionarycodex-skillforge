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
    llm = VertexAI()
    prompt = PromptTemplate(
        input_variables=["job_input"],
        template="Extract skills from the following job description: {job_input}",
    )
    chain = prompt | llm
    skills_string = chain.invoke({"job_input": job_input})
    skills = [s.strip() for s in skills_string.split(",")]
    return skills