# File: README.md
# Wikipedia Article Summarizer

A REST API that fetches any Wikipedia article and returns an AI-generated summary using a transformer model (BART). Falls back to extractive summarization if the model is unavailable.

## Features
- Fetch any Wikipedia article by title
- Generate abstractive summaries using Facebook's BART-large-CNN
- Fallback to extractive summary (first few sentences)
- Simple REST API with FastAPI

## Installation

```bash
git clone <repository>
cd <repository>
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
