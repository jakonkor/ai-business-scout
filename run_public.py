"""
Main pipeline using public APIs and GitHub Models
No proprietary API keys required (except GitHub token for LLM)
"""

import asyncio
import os
import json
from datetime import datetime
from pathlib import Path

from src.agents.public_web_scanner import PublicWebScanner
from src.agents.public_idea_generator import PublicIdeaGenerator
from src.agents.analyst import BusinessAnalystAgent
from src.agents.validator import MarketValidatorAgent


async def run_public_pipeline():
    """
    Run the complete AI Business Scout pipeline using public APIs.
    """
    print("="*80)
    print("🚀 AI BUSINESS SCOUT - PUBLIC API VERSION")
    print("="*80)
    print()
    
    # Check for GitHub token
    github_token = os.getenv("GITHUB_TOKEN")
    if not github_token:
        print("❌ ERROR: GITHUB_TOKEN not found")
        print()
        print("To use this pipeline, you need a GitHub Personal Access Token.")
        print("Get one at: https://github.com/settings/tokens")
        print()
        print("Required scopes: 'public_repo' or 'repo'")
        print()
        print("Then set it in your environment:")
        print("  export GITHUB_TOKEN='your_token_here'")
        print()
        print("Or create a .env file:")
        print("  GITHUB_TOKEN=your_token_here")
        print()
        return
    
    news_api_key = os.getenv("NEWS_API_KEY")
    
    print(f"✅ GitHub Token: Found")
    print(f"{'✅' if news_api_key else 'ℹ️'} NewsAPI Key: {'Found' if news_api_key else 'Not found (optional)'}")
    print()
    
    # Phase 1: Scan for trends
    print("="*80)
    print("PHASE 1: Scanning Public Web Sources")
    print("="*80)
    
    scanner = PublicWebScanner(news_api_key=news_api_key)
    trends = await scanner.scan_all_sources()
    
    if not trends:
        print("❌ No trends found. Check your internet connection.")
        return
    
    print()
    print("Top Trends Discovered:")
    for i, trend in enumerate(scanner.get_top_trends(5), 1):
        print(f"  {i}. {trend.title} ({trend.source.value}) - {trend.engagement:,} engagement")
    print()
    
    # Phase 2: Generate ideas
    print("="*80)
    print("PHASE 2: Generating Business Ideas with GitHub Models")
    print("="*80)
    
    generator = PublicIdeaGenerator(github_token=github_token, model="gpt-4o-mini")
    ideas = await generator.generate_ideas(trends, max_ideas=3)
    
    if not ideas:
        print("❌ No ideas generated.")
        return
    
    print()
    print("Generated Ideas:")
    for i, idea in enumerate(ideas, 1):
        print(f"  {i}. {idea.title}")
        print(f"     {idea.value_proposition}")
    print()
    
    # Phase 3: Analyze ideas
    print("="*80)
    print("PHASE 3: Analyzing Business Viability")
    print("="*80)
    
    analyst = BusinessAnalystAgent()
    analyses = await analyst.analyze_ideas(ideas)
    
    print()
    print("Analysis Results:")
    for i, analysis in enumerate(analyses, 1):
        idea = next(idea for idea in ideas if idea.id == analysis.idea_id)
        print(f"  {i}. {idea.title}: {analysis.viability_score:.1f}/10")
    print()
    
    # Phase 4: Market validation
    print("="*80)
    print("PHASE 4: Market Validation (Simulated Campaigns)")
    print("="*80)
    
    validator = MarketValidatorAgent()
    validations = await validator.validate_ideas(ideas, analyses)
    
    print()
    print("Validation Results:")
    for validation in validations:
        idea = next(idea for idea in ideas if idea.id == validation.idea_id)
        status = "✅ PROMISING" if validation.is_promising else "⚠️ NEEDS WORK"
        print(f"  • {idea.title}: {status}")
        print(f"    Engagement Score: {validation.engagement_score:.1f}/10")
    print()
    
    # Generate report
    print("="*80)
    print("GENERATING REPORT")
    print("="*80)
    
    report = {
        "timestamp": datetime.now().isoformat(),
        "pipeline_version": "public",
        "llm_model": "gpt-4o-mini (GitHub Models)",
        "summary": {
            "trends_found": len(trends),
            "ideas_generated": len(ideas),
            "ideas_validated": len(validations),
            "promising_ideas": sum(1 for v in validations if v.is_promising),
        },
        "trends": [
            {
                "title": t.title,
                "source": t.source.value,
                "engagement": t.engagement,
                "sentiment": t.sentiment,
                "keywords": t.keywords,
            }
            for t in scanner.get_top_trends(10)
        ],
        "ideas": [
            {
                "id": idea.id,
                "title": idea.title,
                "description": idea.description,
                "value_proposition": idea.value_proposition,
                "target_market": idea.target_market,
                "revenue_model": idea.revenue_model,
                "key_features": idea.key_features,
                "analysis": next(
                    (
                        {
                            "viability_score": a.viability_score,
                            "market_size": a.estimated_market_size,
                            "swot": {
                                "strengths": a.strengths,
                                "weaknesses": a.weaknesses,
                                "opportunities": a.opportunities,
                                "threats": a.threats,
                            },
                        }
                        for a in analyses if a.idea_id == idea.id
                    ),
                    None
                ),
                "validation": next(
                    (
                        {
                            "is_promising": v.is_promising,
                            "engagement_score": v.engagement_score,
                            "confidence_level": v.confidence_level,
                            "recommendation": v.recommendation,
                            "campaigns": [
                                {
                                    "platform": c.platform,
                                    "metrics": {
                                        "impressions": c.impressions,
                                        "clicks": c.clicks,
                                        "ctr": c.ctr,
                                        "conversions": c.conversions,
                                        "cpc": c.cost_per_click,
                                    }
                                }
                                for c in v.campaigns
                            ]
                        }
                        for v in validations if v.idea_id == idea.id
                    ),
                    None
                ),
            }
            for idea in ideas
        ],
    }
    
    # Save report
    data_dir = Path("data")
    data_dir.mkdir(exist_ok=True)
    
    report_file = data_dir / f"public_scout_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    
    with open(report_file, 'w') as f:
        json.dump(report, f, indent=2)
    
    print(f"✅ Report saved to: {report_file}")
    print()
    
    # Print executive summary
    print("="*80)
    print("📊 EXECUTIVE SUMMARY")
    print("="*80)
    print()
    print(f"Trends Analyzed:     {len(trends)}")
    print(f"Ideas Generated:     {len(ideas)}")
    print(f"Ideas Validated:     {len(validations)}")
    print(f"Promising Ideas:     {sum(1 for v in validations if v.is_promising)}")
    print()
    print("🎯 Top Recommendations:")
    print()
    
    for validation in sorted(validations, key=lambda v: v.engagement_score, reverse=True)[:3]:
        idea = next(idea for idea in ideas if idea.id == validation.idea_id)
        analysis = next(a for a in analyses if a.idea_id == idea.id)
        
        status = "✅ RECOMMEND" if validation.is_promising else "⚠️ REVISE"
        print(f"  {status}: {idea.title}")
        print(f"  Viability: {analysis.viability_score:.1f}/10 | Engagement: {validation.engagement_score:.1f}/10")
        print(f"  → {validation.recommendation}")
        print()
    
    print("="*80)
    print("✅ Pipeline complete!")
    print("="*80)


if __name__ == "__main__":
    from dotenv import load_dotenv
    load_dotenv()
    
    asyncio.run(run_public_pipeline())
