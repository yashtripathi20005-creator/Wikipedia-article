# File: wiki_summarizer/wikipedia_client.py
"""
Client for fetching article content from Wikipedia.
"""
import requests
from bs4 import BeautifulSoup

class WikipediaClient:
    """
    Handles API requests to Wikipedia and extracts the main article text.
    """
    BASE_URL = "https://en.wikipedia.org/w/api.php"

    @staticmethod
    def fetch_article(title: str) -> str:
        """
        Fetch the plain text content of a Wikipedia article by title.
        :param title: The title of the Wikipedia article.
        :return: The article text as a string.
        :raises ValueError: If the article does not exist or cannot be retrieved.
        """
        params = {
            "action": "parse",
            "page": title,
            "format": "json",
            "prop": "text",
            "redirects": True
        }
        try:
            response = requests.get(WikipediaClient.BASE_URL, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()
        except (requests.RequestException, ValueError) as e:
            raise ValueError(f"Network or JSON error: {e}")

        if "error" in data:
            raise ValueError(f"Wikipedia API error: {data['error'].get('info', 'Unknown error')}")

        if "parse" not in data or "text" not in data["parse"]:
            raise ValueError(f"Article '{title}' not found.")

        html_content = data["parse"]["text"]["*"]
        # Use BeautifulSoup to extract text from the HTML
        soup = BeautifulSoup(html_content, "html.parser")
        # Remove unwanted tags like tables, infoboxes, etc.
        for tag in soup(["table", "span", "div", "sup", "ol", "ul", "figure"]):
            tag.decompose()
        text = soup.get_text(separator="\n")
        # Clean up whitespace
        lines = (line.strip() for line in text.splitlines() if line.strip())
        article_text = "\n".join(lines)

        if not article_text:
            raise ValueError(f"Article '{title}' appears to be empty.")
        return article_text
