# skillforge/backend/services/content_gen.py
from langchain.llms import VertexAI
from langchain.prompts import PromptTemplate

def generate_content(topic: str):
    llm = VertexAI()
    prompt = PromptTemplate(
        input_variables=["topic"],
        template="Explain {topic} in detail.",
    )
    chain = prompt | llm
    content = chain.invoke({"topic": topic})
    return content