"""Web Scraper Tool for AI News Collection."""

import requests
from bs4 import BeautifulSoup
from crewai.tools import BaseTool
from pydantic import Field
from typing import Type, Optional, List, Dict, Any
from pydantic import BaseModel
import re
from datetime import datetime


class ScraperInput(BaseModel):
    """Input schema for the scraper tool."""

    url: str = Field(description="The URL to scrape for AI news")
    max_articles: int = Field(
        default=10, description="Maximum number of articles to collect"
    )


class AINewsScraper(BaseTool):
    """Tool for scraping AI news from various sources."""

    name: str = "ai_news_scraper"
    description: str = """
    Scrapes AI news articles from a given URL.
    Returns a list of articles with titles, descriptions, and links.
    Use this tool to collect news from AI news websites.
    """
    args_schema: Type[BaseModel] = ScraperInput

    def _run(self, url: str, max_articles: int = 10) -> str:
        """Execute the scraping operation.

        Args:
            url: The URL to scrape
            max_articles: Maximum number of articles to return

        Returns:
            Formatted string with scraped articles
        """
        try:
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
            }
            response = requests.get(url, headers=headers, timeout=15)
            response.raise_for_status()

            soup = BeautifulSoup(response.content, "lxml")
            articles = self._extract_articles(soup, url, max_articles)

            if not articles:
                return f"No articles found at {url}"

            return self._format_articles(articles)

        except requests.RequestException as e:
            return f"Error scraping {url}: {str(e)}"
        except Exception as e:
            return f"Unexpected error: {str(e)}"

    def _extract_articles(
        self, soup: BeautifulSoup, base_url: str, max_articles: int
    ) -> List[Dict[str, Any]]:
        """Extract articles from parsed HTML.

        Args:
            soup: BeautifulSoup parsed HTML
            base_url: The base URL for resolving relative links
            max_articles: Maximum number of articles

        Returns:
            List of article dictionaries
        """
        articles = []

        # Common article selectors for news sites
        article_selectors = [
            "article",
            ".post",
            ".article",
            ".news-item",
            ".story",
            ".entry",
            '[class*="article"]',
            '[class*="post"]',
            ".c-entry-box--compact",
            ".river-item",
        ]

        for selector in article_selectors:
            elements = soup.select(selector)
            if elements:
                for element in elements[:max_articles]:
                    article = self._parse_article_element(element, base_url)
                    if article and article.get("title"):
                        articles.append(article)
                        if len(articles) >= max_articles:
                            break
                break

        # Fallback: look for headline links
        if not articles:
            headlines = soup.find_all(["h1", "h2", "h3"], limit=max_articles * 2)
            for headline in headlines:
                link = headline.find("a") or headline.find_parent("a")
                if link and link.get("href"):
                    title = headline.get_text(strip=True)
                    if title and len(title) > 10:
                        href = link.get("href", "")
                        if not href.startswith("http"):
                            href = self._resolve_url(base_url, href)
                        articles.append(
                            {
                                "title": title,
                                "url": href,
                                "description": "",
                                "date": datetime.now().strftime("%Y-%m-%d"),
                            }
                        )
                        if len(articles) >= max_articles:
                            break

        return articles

    def _parse_article_element(
        self, element: BeautifulSoup, base_url: str
    ) -> Optional[Dict[str, Any]]:
        """Parse a single article element.

        Args:
            element: BeautifulSoup element containing article
            base_url: Base URL for resolving links

        Returns:
            Article dictionary or None
        """
        article = {}

        # Extract title
        title_elem = element.find(["h1", "h2", "h3", "h4"]) or element.find(
            class_=re.compile(r"title|headline", re.I)
        )
        if title_elem:
            article["title"] = title_elem.get_text(strip=True)

        # Extract link
        link = element.find("a")
        if link and link.get("href"):
            href = link.get("href", "")
            if not href.startswith("http"):
                href = self._resolve_url(base_url, href)
            article["url"] = href

        # Extract description/summary
        desc_elem = element.find(class_=re.compile(r"desc|summary|excerpt|teaser", re.I))
        if desc_elem:
            article["description"] = desc_elem.get_text(strip=True)[:300]
        else:
            # Try to get first paragraph
            p = element.find("p")
            if p:
                article["description"] = p.get_text(strip=True)[:300]

        # Extract date
        date_elem = element.find("time") or element.find(
            class_=re.compile(r"date|time|published", re.I)
        )
        if date_elem:
            article["date"] = date_elem.get_text(strip=True)
        else:
            article["date"] = datetime.now().strftime("%Y-%m-%d")

        return article if article.get("title") else None

    def _resolve_url(self, base_url: str, relative_url: str) -> str:
        """Resolve a relative URL against a base URL.

        Args:
            base_url: The base URL
            relative_url: The relative URL to resolve

        Returns:
            Absolute URL
        """
        from urllib.parse import urljoin

        return urljoin(base_url, relative_url)

    def _format_articles(self, articles: List[Dict[str, Any]]) -> str:
        """Format articles into a readable string.

        Args:
            articles: List of article dictionaries

        Returns:
            Formatted string
        """
        output = []
        output.append(f"Found {len(articles)} articles:\n")

        for i, article in enumerate(articles, 1):
            output.append(f"--- Article {i} ---")
            output.append(f"Title: {article.get('title', 'N/A')}")
            output.append(f"URL: {article.get('url', 'N/A')}")
            if article.get("description"):
                output.append(f"Description: {article['description']}")
            output.append(f"Date: {article.get('date', 'N/A')}")
            output.append("")

        return "\n".join(output)
