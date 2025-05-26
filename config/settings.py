"""
Application configuration settings
"""
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Supabase Configuration
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

# OpenAI Configuration
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Naver API Configuration
NAVER_CLIENT_ID = os.getenv("NAVER_CLIENT_ID")
NAVER_CLIENT_SECRET = os.getenv("NAVER_CLIENT_SECRET")

# LangSmith Configuration (Optional)
LANGSMITH_API_KEY = os.getenv("LANGSMITH_API_KEY")

# LangSmith setup
if LANGSMITH_API_KEY:
    os.environ["LANGCHAIN_TRACING_V2"] = "true"
    os.environ["LANGCHAIN_PROJECT"] = "smart-shopping-app"
    os.environ["LANGCHAIN_API_KEY"] = LANGSMITH_API_KEY
else:
    os.environ["LANGCHAIN_TRACING_V2"] = "false"
