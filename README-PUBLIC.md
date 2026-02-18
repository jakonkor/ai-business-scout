# 🌐 AI Business Scout - Public API Version

Run the complete AI Business Scout pipeline using **free public APIs** and **GitHub Models**!

## 🎯 What This Uses

### Free Data Sources (No Auth Required)
- ✅ **Hacker News API** - Top tech stories and discussions
- ✅ **Reddit JSON API** - Public posts from tech subreddits
- ✅ **GitHub Trending** - Trending repositories

### Optional Free Tier
- 🔑 **NewsAPI** - Tech news (100 requests/day free)

### LLM Provider
- 🤖 **GitHub Models API** - Free access to:
  - GPT-4o & GPT-4o-mini (OpenAI)
  - Claude 3.5 Sonnet (Anthropic)
  - Llama 3.1 (Meta)
  - Mistral Large
  - Phi-3 (Microsoft)

## 🚀 Quick Start (5 Minutes)

### 1. Install Dependencies

```bash
# Install minimal requirements
pip install -r requirements-public.txt
```

### 2. Get GitHub Token

1. Go to https://github.com/settings/tokens
2. Click "Generate new token (classic)"
3. Give it a name like "AI Business Scout"
4. Select scopes: `public_repo` or `repo`
5. Click "Generate token"
6. Copy the token

### 3. Configure Environment

```bash
# Copy the example file
cp .env.public.example .env

# Edit .env and add your token
nano .env
```

Add this line:
```
GITHUB_TOKEN=ghp_your_token_here
```

### 4. Run the Pipeline!

```bash
python3 run_public.py
```

## 📊 What You'll Get

The pipeline will:

1. **Scan Public Sources** → Find trending topics from HN, Reddit, GitHub
2. **Generate Ideas** → Use GitHub Models to create business ideas
3. **Analyze Viability** → Run SWOT analysis and market sizing
4. **Validate Market** → Simulate ad campaigns with metrics
5. **Generate Report** → Create detailed JSON report

### Sample Output

```
🚀 AI BUSINESS SCOUT - PUBLIC API VERSION
================================================

✅ GitHub Token: Found
ℹ️ NewsAPI Key: Not found (optional)

PHASE 1: Scanning Public Web Sources
================================================
  📰 Scanning Hacker News...
  🤖 Scanning Reddit (public)...
  🐙 Scanning GitHub Trending...

Top Trends Discovered:
  1. AI Code Assistants Trending (news) - 15,240 engagement
  2. WebAssembly Runtime Performance (reddit) - 8,450 engagement
  3. GitHub: microsoft/autogen (google_trends) - 12,500 engagement

PHASE 2: Generating Business Ideas with GitHub Models
================================================
💡 Idea Generator Agent: Generating up to 3 ideas from 15 trends...
   Using model: gpt-4o-mini

Generated Ideas:
  1. AI-Powered Code Review Assistant
     Reduce code review time by 50% using intelligent analysis
  2. WebAssembly Development Platform
     Build and deploy high-performance web applications easily
  3. Multi-Agent Collaboration Tool
     Enable AI agents to work together on complex tasks

PHASE 3: Analyzing Business Viability
================================================
Analysis Results:
  1. AI-Powered Code Review Assistant: 7.2/10
  2. WebAssembly Development Platform: 6.8/10
  3. Multi-Agent Collaboration Tool: 7.5/10

PHASE 4: Market Validation (Simulated Campaigns)
================================================
Validation Results:
  • AI-Powered Code Review Assistant: ✅ PROMISING
    Engagement Score: 7.8/10
  • WebAssembly Development Platform: ⚠️ NEEDS WORK
    Engagement Score: 5.2/10
  • Multi-Agent Collaboration Tool: ✅ PROMISING
    Engagement Score: 8.1/10

📊 EXECUTIVE SUMMARY
================================================
Trends Analyzed:     15
Ideas Generated:     3
Ideas Validated:     3
Promising Ideas:     2

🎯 Top Recommendations:
  ✅ RECOMMEND: Multi-Agent Collaboration Tool
  Viability: 7.5/10 | Engagement: 8.1/10
  → Proceed with MVP development and beta testing
```

## 🔧 Advanced Configuration

### Use Different LLM Models

Edit `run_public.py` and change the model:

```python
generator = PublicIdeaGenerator(
    github_token=github_token, 
    model="gpt-4o"  # or "claude-3.5-sonnet", "llama-3.1-405b", etc.
)
```

### Add NewsAPI (Optional)

1. Get free key at https://newsapi.org/
2. Add to `.env`:
   ```
   NEWS_API_KEY=your_key_here
   ```

### Adjust Number of Ideas

Edit `run_public.py`:
```python
ideas = await generator.generate_ideas(trends, max_ideas=5)  # Generate 5 ideas
```

## 🧪 Test Individual Components

### Test Web Scanner
```bash
python3 -m src.agents.public_web_scanner
```

### Test Idea Generator
```bash
python3 -m src.agents.public_idea_generator
```

### Test GitHub LLM
```bash
python3 -m src.utils.github_llm
```

## 💰 Cost & Rate Limits

### Completely Free
- Hacker News API: Unlimited
- Reddit JSON API: ~60 requests/minute
- GitHub Trending: Unlimited (scraping)

### Free Tier
- GitHub Models: Generous free tier for personal use
- NewsAPI: 100 requests/day free

### Estimated Usage
- One pipeline run: ~5-10 API calls
- Cost: **$0** with free tiers

## 🔒 Privacy & Security

- ✅ All data sources are public
- ✅ No personal data collected
- ✅ GitHub token only used for LLM access
- ✅ No data sent to third parties (except GitHub for LLM)

## 🐛 Troubleshooting

### "GITHUB_TOKEN not found"
- Make sure `.env` file exists in project root
- Check token is valid at https://github.com/settings/tokens
- Try: `export GITHUB_TOKEN=your_token_here`

### "Error calling GitHub Models API"
- Verify token has correct scopes
- Check you're not rate limited
- Try using `gpt-4o-mini` instead of `gpt-4o`

### "No trends found"
- Check internet connection
- Some sources might be temporarily unavailable
- Pipeline will work with whatever sources are available

### Rate Limits
- GitHub Models: Wait a few minutes between runs
- Reddit: Max ~60 requests/minute
- If you hit limits, reduce `max_ideas` parameter

## 📚 Available LLM Models

| Model | Provider | Speed | Quality |
|-------|----------|-------|---------|
| gpt-4o-mini | OpenAI | ⚡⚡⚡ Fast | ⭐⭐⭐ Good |
| gpt-4o | OpenAI | ⚡⚡ Medium | ⭐⭐⭐⭐⭐ Excellent |
| claude-3.5-sonnet | Anthropic | ⚡⚡ Medium | ⭐⭐⭐⭐⭐ Excellent |
| llama-3.1-405b | Meta | ⚡ Slow | ⭐⭐⭐⭐ Very Good |
| mistral-large | Mistral | ⚡⚡ Medium | ⭐⭐⭐⭐ Very Good |

**Recommended:** Start with `gpt-4o-mini` for speed, upgrade to `gpt-4o` or `claude-3.5-sonnet` for better quality.

## 🎓 What You're Learning

This implementation demonstrates:
- ✅ Using free public APIs for data collection
- ✅ Integrating GitHub Models for LLM access
- ✅ Building multi-agent pipelines
- ✅ Async programming in Python
- ✅ Business analysis frameworks (SWOT, market sizing)
- ✅ Data-driven decision making

## 🚀 Next Steps

1. **Run Your First Scan**: `python3 run_public.py`
2. **Review Generated Report**: Check `data/` directory
3. **Experiment with Models**: Try different LLMs
4. **Customize Prompts**: Edit idea generation prompts
5. **Add Data Sources**: Integrate more public APIs

## 📞 Support

- **GitHub**: Issues and pull requests welcome
- **Docs**: See main README.md for full documentation
- **Examples**: Check `data/` for sample reports

---

**Start discovering business opportunities with free AI tools! 🎉**
