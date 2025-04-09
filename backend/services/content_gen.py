from langchain_google_vertexai import VertexAI
from langchain.prompts import PromptTemplate
from google.cloud import texttospeech
import os

# Ensure the environment variable is set
SERVICE_ACCOUNT_FILE = "C:\\Users\\Arunachaleshwar\\Desktop\\key.json"
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = SERVICE_ACCOUNT_FILE

def generate_content(topic: str):
    """
    Generates content for a given topic.

    Args:
        topic (str): The topic to generate content for.

    Returns:
        str: The generated content.
    """
    llm = VertexAI(
        model="gemini-2.0-flash-001",
        project="platinum-scout-456204-j6",
        location="us-central1",
    )  # Uses the service account key for authentication
    prompt = PromptTemplate(
        input_variables=["topic"],
        template="Explain {topic} in detail.",
    )
    chain = prompt | llm
    content = chain.invoke({"topic": topic})
    return content

def generate_audio(content, topic):
    """
    Generates audio from text content.

    Args:
        content (str): The text content to convert to audio.
        topic (str): The topic of the content (used for filename).

    Returns:
        str: The filename of the generated audio file.
    """
    client = texttospeech.TextToSpeechClient()  # Uses the service account key for authentication
    synthesis_input = texttospeech.SynthesisInput(text=content)
    voice = texttospeech.VoiceSelectionParams(language_code="en-US", ssml_gender=texttospeech.SsmlVoiceGender.NEUTRAL)
    audio_config = texttospeech.AudioConfig(audio_encoding=texttospeech.AudioEncoding.MP3)
    response = client.synthesize_speech(input=synthesis_input, voice=voice, audio_config=audio_config)
    file_name = f"{topic.replace(' ', '_')}.mp3"
    with open(file_name, "wb") as out:
        out.write(response.audio_content)
    return file_name