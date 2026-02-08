"""Summarizer Agent - Generates concise summaries using Ollama."""

from crewai import Agent


def create_summarizer_agent(llm) -> Agent:
    """Create the summarizer agent.

    Args:
        llm: The language model to use (Ollama/Llama3)

    Returns:
        Agent configured for summarization
    """
    return Agent(
        role="AI News Summarizer",
        goal="Create concise, informative summaries of AI news articles",
        backstory="""You are a skilled technical writer with deep expertise in
        artificial intelligence. You excel at distilling complex technical content
        into clear, accessible summaries. You understand the nuances of AI research,
        industry developments, and can identify the key takeaways from any article.
        Your summaries are always accurate, balanced, and capture the essential
        information without losing important technical details.""",
        llm=llm,
        verbose=True,
        allow_delegation=False,
    )
