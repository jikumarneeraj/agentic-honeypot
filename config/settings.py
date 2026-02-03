import os

# 🔐 Honeypot API Key (from environment)
API_KEY = os.getenv("API_KEY")

# 🤖 LLM configuration (optional)
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_BASE_URL = os.getenv("OPENAI_BASE_URL", "https://api.openai.com/v1")

MODEL_NAME = "gpt-3.5-turbo"
MAX_TURNS = 8

GUVI_CALLBACK_URL = "https://hackathon.guvi.in/api/updateHoneyPotFinalResult"
