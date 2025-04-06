# skillforge/backend/services/learning_path.py
from langchain.llms import VertexAI
from langchain.prompts import PromptTemplate

def generate_learning_path(skills: list):
    llm = VertexAI()
    prompt = PromptTemplate(
        input_variables=["skills"],
        template="Create a learning path for these skills: {skills}",
    )
    chain = prompt | llm
    path_string = chain.invoke({"skills": ", ".join(skills)})
    path = [p.strip() for p in path_string.split("\n")]
    return path