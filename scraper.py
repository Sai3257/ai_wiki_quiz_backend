import requests
from bs4 import BeautifulSoup
from typing import Dict, Optional


def scrape_wikipedia(url: str) -> Dict[str, str]:
    """
    Scrape Wikipedia article content from the given URL.
    
    Args:
        url: Wikipedia article URL
        
    Returns:
        Dictionary containing 'title' and 'content' of the article
        
    Raises:
        ValueError: If URL is not a valid Wikipedia URL
        requests.RequestException: If request fails
    """
    # Validate Wikipedia URL
    if "wikipedia.org" not in url:
        raise ValueError("URL must be a Wikipedia article")
    
    # Set headers to mimic a browser request
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    
    try:
        # Make request to Wikipedia
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        
        # Parse HTML content
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Extract title
        title_tag = soup.find('h1', class_='firstHeading')
        if not title_tag:
            title_tag = soup.find('h1', id='firstHeading')
        title = title_tag.get_text().strip() if title_tag else "Unknown Title"
        
        # Extract main content
        content_div = soup.find('div', id='mw-content-text')
        if not content_div:
            raise ValueError("Could not find article content")
        
        # Get all paragraphs from the content
        paragraphs = content_div.find_all('p', recursive=True)
        
        # Filter out empty paragraphs and combine
        content_parts = []
        for p in paragraphs:
            text = p.get_text().strip()
            # Skip very short paragraphs (likely navigation or metadata)
            if len(text) > 50:
                content_parts.append(text)
        
        content = "\n\n".join(content_parts)
        
        if not content:
            raise ValueError("No content found in the article")
        
        # Limit content to first 5000 characters to avoid token limits
        if len(content) > 5000:
            content = content[:5000] + "..."
        
        return {
            "title": title,
            "content": content
        }
        
    except requests.RequestException as e:
        raise requests.RequestException(f"Failed to fetch Wikipedia article: {str(e)}")
    except Exception as e:
        raise Exception(f"Error scraping Wikipedia: {str(e)}")


def validate_wikipedia_url(url: str) -> bool:
    """
    Validate if the URL is a proper Wikipedia article URL.
    
    Args:
        url: URL to validate
        
    Returns:
        True if valid Wikipedia URL, False otherwise
    """
    return "wikipedia.org/wiki/" in url and url.startswith("http")
