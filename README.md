# AI Business Scout

AI-powered business idea generator with web scraping, strategic analysis, and market validation.

## Overview

AI Business Scout is a multi-agent system that:
1. **Scans** internet sources (X/Twitter, news sites, Reddit, etc.) for trending topics and market signals
2. **Generates** business ideas based on discovered trends and opportunities
3. **Analyzes** ideas through a business strategist agent using frameworks like SWOT, Porter's Five Forces
4. **Validates** ideas through pre-market testing with Meta/Google Ads campaigns

## Architecture

The system consists of four main agents:

### 1. Web Scanner Agent
- Monitors X/Twitter, Reddit, news sources, and trend platforms
- Identifies emerging trends, pain points, and market opportunities
- Extracts relevant signals and sentiment

### 2. Idea Generator Agent
- Synthesizes trends into concrete business ideas
- Generates value propositions and target market definitions
- Creates multiple idea variations

### 3. Business Analyst Agent
- Performs strategic analysis (SWOT, competitive landscape)
- Evaluates market size, potential revenue, and risks
- Scores and ranks ideas based on viability

### 4. Market Validator Agent
- Designs and launches test campaigns on Meta/Google Ads
- Monitors engagement metrics (CTR, CPC, conversions)
- Provides data-driven validation feedback

## Tech Stack

- **Python 3.11+**
- **Pi SDK** - Multi-agent orchestration
- **Google ADK** - Additional AI capabilities
- **BeautifulSoup/Scrapy** - Web scraping
- **Tweepy** - Twitter/X API integration
- **PRAW** - Reddit API integration
- **Meta Business SDK** - Facebook/Instagram Ads
- **Google Ads API** - Google Ads integration

## Project Structure

```
ai-business-scout/
├── src/
│   ├── agents/
│   │   ├── __init__.py
│   │   ├── web_scanner.py      # Web scraping agent
│   │   ├── idea_generator.py   # Business idea generation
│   │   ├── analyst.py           # Strategic analysis agent
│   │   └── validator.py         # Market validation agent
│   ├── scrapers/
│   │   ├── __init__.py
│   │   ├── twitter_scraper.py
│   │   ├── reddit_scraper.py
│   │   └── news_scraper.py
│   ├── validators/
│   │   ├── __init__.py
│   │   ├── meta_ads.py
│   │   └── google_ads.py
│   ├── models/
│   │   ├── __init__.py
│   │   └── schemas.py           # Data models
│   └── utils/
│       ├── __init__.py
│       └── config.py
├── tests/
├── data/                        # Scraped data and results
├── config/
│   └── config.yaml
├── requirements.txt
├── .env.example
├── .gitignore
└── README.md
```

## Installation

```bash
# Clone the repository
git clone git@github.com:jakonkor/ai-business-scout.git
cd ai-business-scout

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Copy and configure environment variables
cp .env.example .env
# Edit .env with your API keys
```

## Configuration

Required API keys in `.env`:
- `OPENAI_API_KEY` or `ANTHROPIC_API_KEY` - For Pi SDK
- `TWITTER_API_KEY` - Twitter/X API access
- `TWITTER_API_SECRET`
- `REDDIT_CLIENT_ID` - Reddit API access
- `REDDIT_CLIENT_SECRET`
- `META_ACCESS_TOKEN` - Meta Business API
- `GOOGLE_ADS_DEVELOPER_TOKEN` - Google Ads API

## Usage

```bash
# Run the full pipeline
python -m src.main

# Run individual agents
python -m src.agents.web_scanner
python -m src.agents.idea_generator
python -m src.agents.analyst
python -m src.agents.validator
```

## Workflow

1. **Scanning Phase**: Web Scanner Agent monitors sources and collects trends
2. **Generation Phase**: Idea Generator creates business concepts
3. **Analysis Phase**: Business Analyst evaluates and scores ideas
4. **Validation Phase**: Market Validator runs test campaigns
5. **Reporting**: Generate comprehensive report with recommendations

## Roadmap

- [x] Project setup
- [ ] Implement Web Scanner Agent
- [ ] Implement Idea Generator Agent
- [ ] Implement Business Analyst Agent
- [ ] Implement Market Validator Agent
- [ ] Add data persistence (database)
- [ ] Create web dashboard for monitoring
- [ ] Add automated scheduling
- [ ] Implement feedback loop for continuous improvement

## License

MIT

## Contributing

Contributions welcome! Please open an issue or submit a pull request.
