import os
from dotenv import load_dotenv

load_dotenv(dotenv_path=".env_var")

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")


EMBEDDING_MODEL = "text-embedding-3-large"
LLM_MODEL = "gpt-4o-mini"
AGENT_MEMORY_DIR = './agent_memory/'
CHROMA_PERSIST_DIR = "./vectorstore/chroma_db"

if __name__=="__main__":
    print(OPENAI_API_KEY)
