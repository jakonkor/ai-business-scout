"""
Business Analyst Agent - Performs strategic analysis of business ideas
"""

import asyncio
from typing import List
import random

from ..models import BusinessIdea, BusinessAnalysis, SWOTAnalysis
from ..utils.config import config


class BusinessAnalystAgent:
    """
    Agent that performs strategic business analysis on generated ideas.
    Uses frameworks like SWOT, Porter's Five Forces, and market sizing.
    """
    
    def __init__(self):
        self.analyses: List[BusinessAnalysis] = []
    
    async def analyze_ideas(self, ideas: List[BusinessIdea]) -> List[BusinessAnalysis]:
        """
        Analyze business ideas using strategic frameworks.
        
        Args:
            ideas: List of business ideas to analyze
        
        Returns:
            List of business analyses
        """
        print(f"\n📊 Business Analyst Agent: Analyzing {len(ideas)} ideas...")
        
        analyses = []
        for idea in ideas:
            analysis = await self._analyze_single_idea(idea)
            analyses.append(analysis)
        
        self.analyses = analyses
        
        # Sort by viability score
        self.analyses.sort(key=lambda a: a.viability_score, reverse=True)
        
        print(f"✅ Business Analyst Agent: Completed {len(analyses)} analyses")
        
        return analyses
    
    async def _analyze_single_idea(self, idea: BusinessIdea) -> BusinessAnalysis:
        """
        Perform comprehensive analysis of a single business idea.
        
        In production, this would use an LLM to:
        1. Conduct SWOT analysis
        2. Analyze competitive landscape
        3. Estimate market size
        4. Assess risks and opportunities
        5. Calculate viability score
        """
        print(f"  🔍 Analyzing: {idea.title}")
        await asyncio.sleep(0.5)  # Simulate LLM analysis
        
        # TODO: Replace with actual LLM-based analysis
        # For now, generate realistic mock analysis
        
        swot = self._generate_swot(idea)
        competitive_landscape = self._analyze_competition(idea)
        market_size = self._estimate_market_size(idea)
        revenue_potential = self._estimate_revenue(idea)
        risk_level = self._assess_risk(idea)
        viability_score = self._calculate_viability_score(swot, competitive_landscape, market_size)
        
        analysis = BusinessAnalysis(
            idea_id=idea.id,
            swot=swot,
            competitive_landscape=competitive_landscape,
            market_size_estimate=market_size,
            revenue_potential=revenue_potential,
            risk_level=risk_level,
            viability_score=viability_score,
            key_assumptions=[
                "Market adoption rate of 5-10% in first year",
                "Customer acquisition cost can be kept below $100",
                "Product-market fit achieved within 6 months",
                "Competition remains fragmented"
            ],
            recommended_next_steps=[
                "Conduct customer interviews with 20-30 target users",
                "Build MVP focusing on core features",
                "Run market validation campaigns with $1000-2000 budget",
                "Identify and reach out to potential early adopters"
            ]
        )
        
        return analysis
    
    def _generate_swot(self, idea: BusinessIdea) -> SWOTAnalysis:
        """Generate SWOT analysis"""
        # Mock SWOT based on idea characteristics
        return SWOTAnalysis(
            strengths=[
                "Addresses clear market pain point",
                "Scalable SaaS model",
                "Low initial development costs",
                "Strong value proposition"
            ],
            weaknesses=[
                "Unproven market demand",
                "Limited brand recognition",
                "Dependency on third-party platforms",
                "Small initial team"
            ],
            opportunities=[
                "Growing market trend",
                "Potential for rapid user acquisition",
                "Expansion to adjacent markets",
                "Strategic partnerships possible"
            ],
            threats=[
                "Established competitors may enter space",
                "Market preferences could shift",
                "Regulatory changes",
                "Economic downturn affecting B2B spending"
            ]
        )
    
    def _analyze_competition(self, idea: BusinessIdea) -> str:
        """Analyze competitive landscape"""
        competitors = [
            "moderate - several established players but no dominant leader",
            "low - emerging market with few direct competitors",
            "high - crowded market requiring strong differentiation",
            "moderate - niche market with specialized competitors"
        ]
        
        landscapes = [
            f"Competition level: {random.choice(competitors)}. "
            f"Key differentiators needed: unique AI capabilities, superior UX, and faster time-to-value. "
            f"Market fragmentation presents opportunity for consolidation.",
            
            f"Competition level: {random.choice(competitors)}. "
            f"Incumbents focus on enterprise, leaving SMB segment underserved. "
            f"Window of opportunity exists for 18-24 months.",
            
            f"Competition level: {random.choice(competitors)}. "
            f"Existing solutions are legacy systems with poor user experience. "
            f"Modern, user-friendly approach could capture significant market share."
        ]
        
        return random.choice(landscapes)
    
    def _estimate_market_size(self, idea: BusinessIdea) -> str:
        """Estimate total addressable market"""
        sizes = [
            "TAM: $5-10B globally, SAM: $500M-1B, SOM: $50-100M in first 3 years",
            "TAM: $1-3B globally, SAM: $200-400M, SOM: $20-50M in first 3 years",
            "TAM: $500M-1B globally, SAM: $100-200M, SOM: $10-20M in first 3 years",
            "TAM: $10B+ globally, SAM: $1-2B, SOM: $100-200M in first 3 years"
        ]
        return random.choice(sizes)
    
    def _estimate_revenue(self, idea: BusinessIdea) -> str:
        """Estimate revenue potential"""
        potentials = [
            "Conservative: $500K ARR Year 1, $2M Year 2, $5M Year 3",
            "Conservative: $300K ARR Year 1, $1.5M Year 2, $4M Year 3",
            "Conservative: $1M ARR Year 1, $3M Year 2, $8M Year 3",
            "Conservative: $200K ARR Year 1, $1M Year 2, $3M Year 3"
        ]
        return random.choice(potentials)
    
    def _assess_risk(self, idea: BusinessIdea) -> str:
        """Assess overall risk level"""
        return random.choice(["low", "medium", "medium", "high"])
    
    def _calculate_viability_score(self, swot: SWOTAnalysis, 
                                   competitive: str, market_size: str) -> float:
        """Calculate viability score from 0-10"""
        # Simple scoring algorithm
        # In production, would use LLM to assess comprehensively
        
        base_score = 5.0
        
        # Adjust based on strengths/weaknesses ratio
        strength_bonus = min(len(swot.strengths) * 0.3, 2.0)
        weakness_penalty = min(len(swot.weaknesses) * 0.2, 1.5)
        
        # Adjust for opportunities
        opportunity_bonus = min(len(swot.opportunities) * 0.2, 1.0)
        
        # Competitive landscape adjustment
        if "low" in competitive.lower():
            competitive_bonus = 1.0
        elif "moderate" in competitive.lower():
            competitive_bonus = 0.5
        else:
            competitive_bonus = 0.0
        
        score = base_score + strength_bonus - weakness_penalty + opportunity_bonus + competitive_bonus
        
        # Clamp between 0 and 10
        return max(0.0, min(10.0, score))
    
    def get_top_ideas(self, limit: int = 3) -> List[BusinessAnalysis]:
        """Get top-ranked ideas by viability score"""
        return self.analyses[:limit]


async def main():
    """Test the Business Analyst Agent"""
    from .web_scanner import WebScannerAgent
    from .idea_generator import IdeaGeneratorAgent
    
    # Scan trends
    scanner = WebScannerAgent()
    trends = await scanner.scan_all_sources()
    
    # Generate ideas
    generator = IdeaGeneratorAgent()
    ideas = await generator.generate_ideas(trends, max_ideas=3)
    
    # Analyze ideas
    analyst = BusinessAnalystAgent()
    analyses = await analyst.analyze_ideas(ideas)
    
    print("\n" + "="*60)
    print("Business Analysis Results (Ranked by Viability):")
    print("="*60)
    
    for i, analysis in enumerate(analyst.get_top_ideas(), 1):
        # Find corresponding idea
        idea = next(idea for idea in ideas if idea.id == analysis.idea_id)
        
        print(f"\n🏆 Rank #{i}: {idea.title}")
        print(f"   Viability Score: {analysis.viability_score:.1f}/10")
        print(f"   Risk Level: {analysis.risk_level.upper()}")
        
        print(f"\n   SWOT Analysis:")
        print(f"     Strengths: {len(analysis.swot.strengths)}")
        for s in analysis.swot.strengths[:2]:
            print(f"       • {s}")
        print(f"     Opportunities: {len(analysis.swot.opportunities)}")
        for o in analysis.swot.opportunities[:2]:
            print(f"       • {o}")
        
        print(f"\n   Market Size: {analysis.market_size_estimate}")
        print(f"   Revenue Potential: {analysis.revenue_potential}")
        
        print(f"\n   Top Recommendation:")
        print(f"     • {analysis.recommended_next_steps[0]}")


if __name__ == "__main__":
    asyncio.run(main())
