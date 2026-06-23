# File: main.py
"""
Entry point for running the FastAPI server.
"""
import uvicorn
from dotenv import load_dotenv
import os

load_dotenv()

if __name__ == "__main__":
    host = os.getenv("API_HOST", "127.0.0.1")
    port = int(os.getenv("API_PORT", 8000))
    uvicorn.run("wiki_summarizer.api:app", host=host, port=port, reload=True)
