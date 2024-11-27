import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    GROQ_API_KEY = os.getenv('GROQ_API_KEY')
    LLM_MODEL = "llama3-8b-8192"
    LLM_TEMPERATURE = 0.7