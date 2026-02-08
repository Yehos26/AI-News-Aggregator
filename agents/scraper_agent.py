"""Web Scraper Agent - Collects AI news from multiple sources."""

from crewai import Agent


def create_scraper_agent(llm, tools: list) -> Agent:
    """Create the web scraper agent.

    Args:
        llm: The language model to use
        tools: List of scraping tools

    Returns:
        Agent configured for web scraping
    """
    return Agent(
        role="AI News Web Scraper",
        goal="Collect the latest AI news articles from various reliable sources",
        backstory="""You are an expert web scraper specialized in AI and technology news.
        You have years of experience navigating news websites and extracting relevant
        information. You know how to identify high-quality AI news sources and extract
        the most important details from articles including titles, summaries, dates,
        and source URLs. You are meticulous and always verify the relevance of news
        to artificial intelligence before including it in your collection.""",
        tools=tools,
        llm=llm,
        verbose=True,
        allow_delegation=False,
    )
