"""Task definitions for the AI News Aggregator."""

from crewai import Task, Agent
from tools.news_sources import NEWS_SOURCES, AI_CATEGORIES


def create_scraping_task(agent: Agent) -> Task:
    """Create the web scraping task.

    Args:
        agent: The scraper agent

    Returns:
        Configured scraping task
    """
    sources_list = "\n".join([f"- {s['name']}: {s['url']}" for s in NEWS_SOURCES])

    return Task(
        description=f"""Collect the latest AI news articles from the following sources:

{sources_list}

For each source:
1. Use the ai_news_scraper tool to collect up to 5 articles per source
2. Extract the title, URL, description, and date for each article
3. Focus on articles about artificial intelligence, machine learning, and related topics
4. Ignore articles that are not primarily about AI

Compile all collected articles into a structured list.""",
        expected_output="""A comprehensive list of AI news articles in the following format:

SOURCE: [Source Name]
---
1. Title: [Article Title]
   URL: [Article URL]
   Description: [Brief description]
   Date: [Publication date]

2. Title: ...
   ...

(Continue for all sources and articles)

Total articles collected: [number]""",
        agent=agent,
    )


def create_summarization_task(agent: Agent, context: list) -> Task:
    """Create the summarization task.

    Args:
        agent: The summarizer agent
        context: Previous tasks for context

    Returns:
        Configured summarization task
    """
    return Task(
        description="""Review the collected AI news articles and create concise summaries.

For each article:
1. Read the title and available description
2. Create a 2-3 sentence summary capturing the key points
3. Identify the main topic and significance
4. Note any mentioned companies, technologies, or researchers

Focus on:
- What happened or was announced
- Why it matters for the AI field
- Key technical details if available""",
        expected_output="""Summarized articles in the following format:

ARTICLE SUMMARIES
=================

1. [Original Title]
   Source: [Source Name]
   Summary: [2-3 sentence summary of the key points]
   Key Topics: [Main topics covered]
   Significance: [Why this matters]

2. [Original Title]
   ...

(Continue for all articles)""",
        agent=agent,
        context=context,
    )


def create_categorization_task(agent: Agent, context: list) -> Task:
    """Create the categorization task.

    Args:
        agent: The categorizer agent
        context: Previous tasks for context

    Returns:
        Configured categorization task
    """
    categories_list = "\n".join([f"- {cat}" for cat in AI_CATEGORIES])

    return Task(
        description=f"""Categorize the summarized AI news articles into appropriate topics.

Available categories:
{categories_list}

For each article:
1. Analyze the summary and key topics
2. Assign one primary category
3. Assign up to 2 secondary categories if applicable
4. Group articles by their primary category

Consider:
- The main focus of the article
- Technologies mentioned
- Application domain
- Research vs. industry focus""",
        expected_output="""Categorized articles organized by topic:

CATEGORIZED NEWS
================

## Large Language Models (LLM)
1. [Article Title]
   Summary: [Brief summary]
   Secondary Categories: [If any]

2. ...

## Computer Vision
1. ...

## [Other Categories with Articles]
...

CATEGORY STATISTICS:
- LLM: X articles
- Computer Vision: Y articles
- ...

TRENDING TOPICS: [List of most common themes across articles]""",
        agent=agent,
        context=context,
    )


def create_reporting_task(agent: Agent, context: list) -> Task:
    """Create the reporting task.

    Args:
        agent: The reporter agent
        context: Previous tasks for context

    Returns:
        Configured reporting task
    """
    return Task(
        description="""Create a comprehensive daily AI news report based on the
categorized and summarized articles.

The report should include:
1. Executive Summary - Key highlights of the day
2. Top Stories - The most significant 3-5 news items
3. Category Breakdown - News organized by topic
4. Emerging Trends - Patterns and themes observed
5. Notable Mentions - Companies, researchers, products featured

Make the report:
- Professional and well-structured
- Accessible to both technical and non-technical readers
- Informative with actionable insights
- Properly formatted with clear sections""",
        expected_output="""
# AI NEWS DAILY REPORT
Date: [Current Date]

## EXECUTIVE SUMMARY
[2-3 paragraph overview of the day's most important AI developments]

## TOP STORIES

### 1. [Most Important Story Title]
[Detailed summary with context and implications]
Source: [Source Name] | Category: [Category]

### 2. [Second Important Story]
...

### 3. [Third Important Story]
...

## NEWS BY CATEGORY

### Large Language Models
- [Story 1 brief]
- [Story 2 brief]

### Computer Vision
- ...

[Continue for each category with articles]

## EMERGING TRENDS
1. [Trend 1]: [Brief explanation]
2. [Trend 2]: [Brief explanation]
...

## NOTABLE MENTIONS
- **Companies**: [List of companies mentioned]
- **Technologies**: [Key technologies discussed]
- **Researchers/Figures**: [Notable people mentioned]

## STATISTICS
- Total Articles Analyzed: [Number]
- Sources Covered: [Number]
- Categories Represented: [Number]

---
Report generated by AI News Aggregator
Powered by CrewAI + Ollama (Llama 3)
""",
        agent=agent,
        context=context,
        output_file="outputs/daily_report.md",
    )
