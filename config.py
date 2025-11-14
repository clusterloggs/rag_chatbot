import os
from dotenv import load_dotenv

load_dotenv()

INDEX_PATH = os.getenv('FAISS_INDEX_PATH', 'faiss_index')
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

if not OPENAI_API_KEY:
    raise EnvironmentError("OPENAI_API_KEY must be set in the environment")