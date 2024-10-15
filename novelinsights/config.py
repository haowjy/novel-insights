# config.py

from dotenv import load_dotenv
import os

load_dotenv()

class Config:
    def __init__(self):
        self.OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
        self.ANTROPIC_API_KEY = os.getenv("ANTROPIC_API_KEY")
        self.QDRANT_URL = os.getenv("QDRANT_URL")