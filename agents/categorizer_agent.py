"""Categorizer Agent - Organizes news by topics."""

from crewai import Agent


def create_categorizer_agent(llm) -> Agent:
    """Create the categorizer agent.

    Args:
        llm: The language model to use

    Returns:
        Agent configured for categorization
    """
    return Agent(
        role="AI News Categorizer",
        goal="Accurately categorize AI news articles into relevant topics",
        backstory="""You are an AI taxonomy expert with comprehensive knowledge of
        the artificial intelligence field. You understand the distinctions between
        different AI subfields including Large Language Models (LLM), Computer Vision,
        Natural Language Processing (NLP), Reinforcement Learning, Robotics, AI Ethics,
        AI Business & Industry, and AI Research. You can quickly analyze content and
        assign appropriate categories based on the primary focus of each article.
        You also identify emerging trends and cross-disciplinary topics.""",
        llm=llm,
        verbose=True,
        allow_delegation=False,
    )
