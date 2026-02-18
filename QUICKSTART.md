# Quick Start Guide

## Setup (5 minutes)

### 1. Clone and Install

```bash
git clone git@github.com:jakonkor/ai-business-scout.git
cd ai-business-scout

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Configure API Keys

```bash
# Copy example environment file
cp .env.example .env

# Edit .env and add your API keys
# At minimum, you need ONE AI provider:
# - OPENAI_API_KEY (recommended) or
# - ANTHROPIC_API_KEY
```

### 3. Run Demo

```bash
# Run the full pipeline with mock data
python -m src.main
```

This will:
1. ✅ Scan web sources for trends (using mock data initially)
2. ✅ Generate business ideas from trends
3. ✅ Analyze ideas using business frameworks
4. ✅ Validate ideas through simulated ad campaigns
5. ✅ Generate comprehensive report

### 4. Test Individual Agents

```bash
# Test Web Scanner
python -m src.agents.web_scanner

# Test Idea Generator
python -m src.agents.idea_generator

# Test Business Analyst
python -m src.agents.analyst

# Test Market Validator
python -m src.agents.validator
```

## Next Steps

### Enable Real Data Sources

1. **Twitter/X**: Add Twitter API keys to scan real tweets
2. **Reddit**: Add Reddit API credentials to scan subreddits
3. **News**: Add News API key for news article scanning
4. **Meta Ads**: Configure Meta Business API for real ad campaigns
5. **Google Ads**: Configure Google Ads API for validation

### Customize the Pipeline

Edit `src/main.py` to customize:
- Number of ideas to generate
- Validation budget per idea
- Campaign duration
- Output format

### Example Usage

```python
from src.main import BusinessScout

scout = BusinessScout()
report = await scout.run_full_pipeline(
    max_ideas=10,
    validation_budget_per_idea=1000.0,
    validation_duration_days=14
)
```

## Architecture Overview

```
┌─────────────────┐
│  Web Scanner    │  Scans X, Reddit, News, Google Trends
│     Agent       │  Identifies trends and signals
└────────┬────────┘
         │ trends
         ▼
┌─────────────────┐
│ Idea Generator  │  Synthesizes trends into business ideas
│     Agent       │  Creates value propositions
└────────┬────────┘
         │ ideas
         ▼
┌─────────────────┐
│ Business        │  Performs SWOT, market analysis
│ Analyst Agent   │  Scores viability
└────────┬────────┘
         │ analyses
         ▼
┌─────────────────┐
│   Market        │  Runs validation campaigns
│ Validator Agent │  Measures real market interest
└────────┬────────┘
         │ results
         ▼
┌─────────────────┐
│ Scout Report    │  Comprehensive recommendations
└─────────────────┘
```

## Sample Output

```
📊 EXECUTIVE SUMMARY
════════════════════════════════════════════════════════

Metric                Value
─────────────────────────────────────────
Trends Analyzed       4
Ideas Generated       3
Ideas Validated       3
Promising Ideas       2

🎯 Top Recommendations:
  🎯 2 out of 3 ideas show strong market validation
  ✨ 'AI-Powered Code Review Assistant' - Viability: 7.2/10, Engagement: 8.1/10
  ✨ 'AI Budget Coach' - Viability: 6.8/10, Engagement: 7.5/10

💡 Top Ideas (by validation):

✅ 1. AI-Powered Code Review Assistant
   Viability Score: 7.2/10
   Engagement Score: 8.1/10
   CTR: 3.45% | Conversions: 87 | CPC: $2.15
   Reduce code review time by 50% and catch bugs before they reach production
```

## Roadmap

- [ ] Integrate real Twitter/X API
- [ ] Integrate real Reddit API  
- [ ] Integrate real News API
- [ ] Implement actual LLM-based idea generation
- [ ] Implement actual LLM-based analysis
- [ ] Connect to real Meta Ads API
- [ ] Connect to real Google Ads API
- [ ] Add database persistence
- [ ] Create web dashboard
- [ ] Add scheduling/automation
- [ ] Implement feedback loops

## Contributing

Pull requests welcome! See issues for planned features.

## Support

For issues or questions, please open a GitHub issue.
