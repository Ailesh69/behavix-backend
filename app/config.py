import os
from dotenv import load_dotenv

base_dir = os.path.dirname(os.path.abspath(__file__))
load_dotenv(os.path.join(base_dir, "..",".env"))

DATABASE_URL = os.getenv("DATABASE_URL")
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = 30
GROQ_API_KEY = os.getenv("GROQ_API_KEY")


if not DATABASE_URL:
    raise ValueError("DATABASE_URL environment variable not set")
if not GROQ_API_KEY:
    raise ValueError("GROQ_API_KEY environment variable not set")


