# File: wiki_summarizer/api.py
"""
FastAPI application providing a REST endpoint for article summarization.
"""
from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel
from typing import Optional
import os

from .wikipedia_client import WikipediaClient
from .summarizer import WikipediaSummarizer

app = FastAPI(title="Wikipedia Article Summarizer")
summarizer = WikipediaSummarizer()

class SummaryResponse(BaseModel):
    title: str
    summary: str
    original_length: int
    summary_length: int

@app.get("/summarize", response_model=SummaryResponse)
async def summarize_article(
    title: str = Query(..., description="Title of the Wikipedia article"),
    max_length: Optional[int] = Query(150, ge=20, le=500, description="Max summary length in words")
):
    """
    Fetch a Wikipedia article and return a summarized version.
    """
    try:
        article_text = WikipediaClient.fetch_article(title)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

    if not article_text:
        raise HTTPException(status_code=404, detail="Article content is empty.")

    # Summarize the article
    summary = summarizer.summarize(article_text, max_length=max_length)

    return SummaryResponse(
        title=title,
        summary=summary,
        original_length=len(article_text.split()),
        summary_length=len(summary.split())
    )

@app.get("/health")
async def health_check():
    return {"status": "healthy"}
