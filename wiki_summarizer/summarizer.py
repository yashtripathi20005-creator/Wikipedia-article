# File: wiki_summarizer/summarizer.py
"""
Core summarization module using a pre-trained transformer model.
"""
from transformers import pipeline

class WikipediaSummarizer:
    """
    A summarizer that uses a pre-trained transformer model to summarize text.
    Falls back to a simple extractive summary if the model is unavailable.
    """
    def __init__(self, model_name="facebook/bart-large-cnn"):
        """
        Initialize the summarizer pipeline.
        :param model_name: Name of the HuggingFace summarization model.
        """
        try:
            self.summarizer = pipeline(
                "summarization",
                model=model_name,
                device=-1  # Use CPU; set to 0 for GPU if available.
            )
            self.model_loaded = True
        except Exception as e:
            print(f"Warning: Could not load summarization model: {e}")
            print("Falling back to a simple extractive summarizer.")
            self.model_loaded = False

    def summarize(self, text: str, max_length: int = 150, min_length: int = 40) -> str:
        """
        Summarize the given text.
        :param text: The text to summarize.
        :param max_length: Maximum length of the summary.
        :param min_length: Minimum length of the summary.
        :return: The summarized text.
        """
        if not text or len(text.split()) < 30:
            return text.strip() or "Text too short to summarize."

        if self.model_loaded:
            try:
                result = self.summarizer(
                    text,
                    max_length=max_length,
                    min_length=min_length,
                    do_sample=False,
                    truncation=True
                )
                return result[0]['summary_text']
            except Exception as e:
                print(f"Model summarization failed: {e}. Using fallback.")
                return self._extractive_summary(text, max_length)
        else:
            return self._extractive_summary(text, max_length)

    def _extractive_summary(self, text: str, max_length: int) -> str:
        """
        A simple extractive summarizer: return the first few sentences up to max_length words.
        """
        sentences = text.replace('\n', ' ').split('. ')
        summary = []
        word_count = 0
        for sent in sentences:
            words = sent.split()
            if word_count + len(words) > max_length:
                break
            summary.append(sent)
            word_count += len(words)
        return '. '.join(summary).strip() + '.'
