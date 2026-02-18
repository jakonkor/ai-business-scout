"""
Public Idea Generator - Uses GitHub Models API for LLM-powered generation
"""

import asyncio
from typing import List
import uuid
import json

from ..models import Trend, BusinessIdea
from ..utils.github_llm import GitHubLLM


class PublicIdeaGenerator:
    """
    Agent that generates business ideas from trends using GitHub Models API.
    Uses free LLM access through GitHub's AI marketplace.
    """
    
    def __init__(self, github_token: str = None, model: str = "gpt-4o-mini"):
        """
        Initialize the idea generator.
        
        Args:
            github_token: GitHub personal access token
            model: LLM model to use (default: gpt-4o-mini)
        """
        self.llm = GitHubLLM(token=github_token, model=model)
        self.ideas: List[BusinessIdea] = []
    
    async def generate_ideas(self, trends: List[Trend], max_ideas: int = 5) -> List[BusinessIdea]:
        """
        Generate business ideas from trends using LLM.
        
        Args:
            trends: List of trends to analyze
            max_ideas: Maximum number of ideas to generate
        
        Returns:
            List of generated business ideas
        """
        print(f"\n💡 Idea Generator Agent: Generating up to {max_ideas} ideas from {len(trends)} trends...")
        print(f"   Using model: {self.llm.model}")
        
        # Group and prioritize trends
        top_trends = self._select_top_trends(trends, max_ideas)
        
        # Generate ideas concurrently
        tasks = [self._generate_idea_from_trend(trend) for trend in top_trends]
        ideas = await asyncio.gather(*tasks, return_exceptions=True)
        
        # Filter out errors
        valid_ideas = [idea for idea in ideas if isinstance(idea, BusinessIdea)]
        
        self.ideas = valid_ideas
        print(f"✅ Idea Generator Agent: Generated {len(valid_ideas)} business ideas")
        
        return valid_ideas
    
    def _select_top_trends(self, trends: List[Trend], limit: int) -> List[Trend]:
        """Select most promising trends based on engagement and sentiment."""
        # Score trends
        scored_trends = []
        for trend in trends:
            score = trend.engagement * (1 + trend.sentiment)
            scored_trends.append((score, trend))
        
        # Sort by score and return top N
        scored_trends.sort(reverse=True, key=lambda x: x[0])
        return [trend for _, trend in scored_trends[:limit]]
    
    async def _generate_idea_from_trend(self, trend: Trend) -> BusinessIdea:
        """
        Generate a single business idea from a trend using LLM.
        
        Args:
            trend: Trend to analyze
        
        Returns:
            Generated business idea
        """
        system_prompt = """You are a business consultant specializing in identifying startup opportunities.
Analyze trends and generate concrete, actionable business ideas.
Focus on problems that can be solved with technology and have clear revenue models."""

        user_prompt = f"""Based on this trend, generate a business idea:

Trend: {trend.title}
Description: {trend.description}
Keywords: {', '.join(trend.keywords[:5])}
Engagement Level: {trend.engagement:,}
Sentiment: {trend.sentiment:+.2f}

Generate a business idea that addresses this trend. Return a JSON object with:
{{
  "title": "Clear, concise business name",
  "description": "1-2 sentence description of the business",
  "value_proposition": "What value does this provide to customers?",
  "target_market": "Who is the ideal customer?",
  "problem_solved": "What specific problem does this solve?",
  "revenue_model": "How will this make money?",
  "key_features": ["feature1", "feature2", "feature3"]
}}

Be specific and practical. Focus on ideas that could be launched in 3-6 months."""

        try:
            # Generate idea using LLM
            response = await self.llm.generate_json(
                prompt=user_prompt,
                system_prompt=system_prompt,
                temperature=0.8,
            )
            
            # Create BusinessIdea object
            idea = BusinessIdea(
                id=str(uuid.uuid4()),
                title=response.get('title', 'Untitled Idea'),
                description=response.get('description', ''),
                value_proposition=response.get('value_proposition', ''),
                target_market=response.get('target_market', ''),
                problem_solved=response.get('problem_solved', ''),
                revenue_model=response.get('revenue_model', ''),
                key_features=response.get('key_features', []),
                source_trends=[trend.id],
            )
            
            return idea
            
        except Exception as e:
            print(f"  ❌ Error generating idea from trend '{trend.title}': {e}")
            
            # Return fallback idea
            return BusinessIdea(
                id=str(uuid.uuid4()),
                title=f"Solution for {trend.keywords[0].title() if trend.keywords else 'Market'} Space",
                description=f"A platform addressing the {trend.title.lower()}",
                value_proposition="Solve key challenges in this emerging market",
                target_market="Early adopters and tech-savvy users",
                problem_solved=trend.description,
                revenue_model="SaaS subscription model",
                key_features=["Feature 1", "Feature 2", "Feature 3"],
                source_trends=[trend.id],
            )


async def main():
    """Test the Public Idea Generator"""
    from .public_web_scanner import PublicWebScanner
    import os
    
    # Check for GitHub token
    github_token = os.getenv("GITHUB_TOKEN")
    if not github_token:
        print("❌ GITHUB_TOKEN not found in environment")
        print("Get a token at: https://github.com/settings/tokens")
        print("\nUsing fallback mode...\n")
        return
    
    # Scan for trends
    scanner = PublicWebScanner()
    trends = await scanner.scan_all_sources()
    
    # Generate ideas
    generator = PublicIdeaGenerator(github_token=github_token)
    ideas = await generator.generate_ideas(trends, max_ideas=3)
    
    print("\n" + "="*60)
    print("Generated Business Ideas:")
    print("="*60)
    
    for i, idea in enumerate(ideas, 1):
        print(f"\n💡 Idea {i}: {idea.title}")
        print(f"   {idea.description}")
        print(f"\n   Value Proposition: {idea.value_proposition}")
        print(f"   Target Market: {idea.target_market}")
        print(f"   Revenue Model: {idea.revenue_model}")
        print(f"\n   Key Features:")
        for feature in idea.key_features:
            print(f"     • {feature}")


if __name__ == "__main__":
    asyncio.run(main())
