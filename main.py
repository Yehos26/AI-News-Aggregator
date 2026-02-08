#!/usr/bin/env python3
"""
AI News Aggregator - Main Entry Point

Multi-agent system that collects, summarizes, and categorizes
the latest AI news using CrewAI and Ollama (Llama 3).

Author: Yunus Emre Hoş
"""

import os
import sys
from datetime import datetime
from pathlib import Path

from crewai import Crew, Process, LLM

from agents import (
    create_scraper_agent,
    create_summarizer_agent,
    create_categorizer_agent,
    create_reporter_agent,
)
from tasks import (
    create_scraping_task,
    create_summarization_task,
    create_categorization_task,
    create_reporting_task,
)
from tools import AINewsScraper


def check_ollama_connection() -> bool:
    """Check if Ollama is running and accessible.

    Returns:
        True if Ollama is accessible, False otherwise
    """
    import requests

    try:
        response = requests.get("http://localhost:11434/api/tags", timeout=5)
        return response.status_code == 200
    except requests.RequestException:
        return False


def create_llm():
    """Create and configure the Ollama LLM.

    Returns:
        Configured LLM instance for Ollama
    """
    return LLM(
        model="ollama/llama3",
        base_url="http://localhost:11434",
        temperature=0.7,
    )


def setup_output_directory():
    """Ensure the outputs directory exists."""
    output_dir = Path("outputs")
    output_dir.mkdir(exist_ok=True)
    return output_dir


def run_news_aggregator():
    """Run the AI News Aggregator crew."""
    print("=" * 60)
    print("   AI NEWS AGGREGATOR")
    print("   Powered by CrewAI + Ollama (Llama 3)")
    print("=" * 60)
    print()

    # Check Ollama connection
    print("[*] Checking Ollama connection...")
    if not check_ollama_connection():
        print("[!] ERROR: Cannot connect to Ollama.")
        print("    Please ensure Ollama is running:")
        print("    1. Install Ollama: https://ollama.ai")
        print("    2. Run: ollama run llama3")
        print("    3. Try again")
        sys.exit(1)
    print("[+] Ollama connection successful!")
    print()

    # Setup
    setup_output_directory()
    llm = create_llm()
    scraper_tool = AINewsScraper()

    # Create agents
    print("[*] Initializing agents...")
    scraper_agent = create_scraper_agent(llm, tools=[scraper_tool])
    summarizer_agent = create_summarizer_agent(llm)
    categorizer_agent = create_categorizer_agent(llm)
    reporter_agent = create_reporter_agent(llm)
    print("[+] Agents initialized!")
    print()

    # Create tasks
    print("[*] Creating tasks...")
    scraping_task = create_scraping_task(scraper_agent)
    summarization_task = create_summarization_task(
        summarizer_agent, context=[scraping_task]
    )
    categorization_task = create_categorization_task(
        categorizer_agent, context=[summarization_task]
    )
    reporting_task = create_reporting_task(
        reporter_agent, context=[categorization_task]
    )
    print("[+] Tasks created!")
    print()

    # Create and run crew
    print("[*] Assembling crew...")
    crew = Crew(
        agents=[scraper_agent, summarizer_agent, categorizer_agent, reporter_agent],
        tasks=[scraping_task, summarization_task, categorization_task, reporting_task],
        process=Process.sequential,
        verbose=True,
    )
    print("[+] Crew assembled!")
    print()

    print("=" * 60)
    print("   STARTING NEWS AGGREGATION")
    print(f"   Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)
    print()

    try:
        result = crew.kickoff()

        print()
        print("=" * 60)
        print("   AGGREGATION COMPLETE")
        print("=" * 60)
        print()
        print(f"[+] Report saved to: outputs/daily_report.md")
        print()
        print("--- FINAL REPORT ---")
        print(result)

        return result

    except KeyboardInterrupt:
        print("\n[!] Aggregation cancelled by user.")
        sys.exit(0)
    except Exception as e:
        print(f"\n[!] Error during aggregation: {e}")
        raise


def main():
    """Main entry point."""
    try:
        run_news_aggregator()
    except Exception as e:
        print(f"[!] Fatal error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
