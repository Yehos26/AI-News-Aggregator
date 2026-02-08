# AI News Aggregator

Multi-agent system that collects, summarizes, and categorizes the latest AI news using CrewAI and local LLM (Ollama).

## Features
- **Web Scraper Agent**: Collects AI news from multiple sources
- **Summarizer Agent**: Generates concise summaries using Ollama (Llama 3)
- **Categorizer Agent**: Organizes news by topics (LLM, Computer Vision, NLP, etc.)
- **Reporter Agent**: Creates daily AI news reports

## Tech Stack
- **Framework**: CrewAI
- **LLM**: Ollama (Llama 3) - local deployment
- **Language**: Python
- **Tools**: BeautifulSoup4, Requests, lxml

## Prerequisites

1. **Python 3.10+** installed
2. **Ollama** installed and running
   - Install from: https://ollama.ai
   - Pull Llama 3: `ollama pull llama3`

## Setup
```bash
# Clone repository
git clone https://github.com/Yehos26/AI-News-Aggregator.git
cd AI-News-Aggregator

# Create virtual environment (recommended)
python -m venv venv
source venv/bin/activate  # Linux/Mac
# or
venv\Scripts\activate  # Windows

# Install dependencies
pip install -r requirements.txt

# Ensure Ollama is running with Llama 3
ollama run llama3

# Run the aggregator
python main.py
```

## Project Structure
```
AI-News-Aggregator/
├── agents/              # Agent definitions
│   ├── __init__.py
│   ├── scraper_agent.py
│   ├── summarizer_agent.py
│   ├── categorizer_agent.py
│   └── reporter_agent.py
├── tasks/               # Task configurations
│   ├── __init__.py
│   └── news_tasks.py
├── tools/               # Custom tools (scrapers, parsers)
│   ├── __init__.py
│   ├── web_scraper.py
│   └── news_sources.py
├── outputs/             # Generated reports
├── main.py              # Entry point
├── requirements.txt
└── README.md
```

## How It Works

1. **Scraping Phase**: The Web Scraper Agent visits configured news sources and collects the latest AI-related articles
2. **Summarization Phase**: The Summarizer Agent processes each article and creates concise summaries
3. **Categorization Phase**: The Categorizer Agent organizes articles into categories (LLM, Computer Vision, NLP, etc.)
4. **Reporting Phase**: The Reporter Agent compiles everything into a comprehensive daily report

## News Sources

Currently configured sources:
- MIT Technology Review - AI
- VentureBeat AI
- The Verge - AI
- Ars Technica - AI
- TechCrunch - AI

## Categories

Articles are categorized into:
- Large Language Models (LLM)
- Computer Vision
- Natural Language Processing (NLP)
- Reinforcement Learning
- Robotics & Automation
- AI Ethics & Safety
- AI Business & Industry
- AI Research & Papers
- Generative AI
- Machine Learning

## Roadmap
- [x] Setup project structure
- [x] Implement scraper agent
- [x] Integrate Ollama for summarization
- [x] Add categorization logic
- [x] Generate daily reports
- [ ] Add more news sources
- [ ] Add scheduling for automatic daily runs
- [ ] Implement news storage/database
- [ ] Add web interface for reports

## Author
**Yunus Emre Hoş**

## License
MIT
