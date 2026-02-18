"""
Market Validator Agent - Validates ideas through ad campaigns
"""

import asyncio
from typing import List, Optional
import random

from ..models import (
    BusinessIdea,
    BusinessAnalysis,
    AdCampaign,
    AdPlatform,
    ValidationMetrics,
    ValidationResult
)
from ..utils.config import config


class MarketValidatorAgent:
    """
    Agent that validates business ideas through market testing.
    Creates and monitors ad campaigns on Meta, Google, etc.
    """
    
    def __init__(self):
        self.campaigns: List[AdCampaign] = []
        self.validations: List[ValidationResult] = []
    
    async def validate_ideas(
        self,
        ideas: List[BusinessIdea],
        analyses: List[BusinessAnalysis],
        budget_per_idea: float = 500.0,
        duration_days: int = 7
    ) -> List[ValidationResult]:
        """
        Validate business ideas through ad campaigns.
        
        Args:
            ideas: Business ideas to validate
            analyses: Corresponding business analyses
            budget_per_idea: Budget allocation per idea
            duration_days: Campaign duration
        
        Returns:
            List of validation results
        """
        print(f"\n🎯 Market Validator Agent: Validating {len(ideas)} ideas...")
        print(f"   Budget per idea: ${budget_per_idea}")
        print(f"   Duration: {duration_days} days")
        
        validations = []
        
        for idea in ideas:
            # Find corresponding analysis
            analysis = next((a for a in analyses if a.idea_id == idea.id), None)
            
            # Create campaign
            campaign = await self._create_campaign(idea, budget_per_idea, duration_days)
            self.campaigns.append(campaign)
            
            # Simulate running campaign
            validation = await self._run_and_analyze_campaign(campaign, idea, analysis)
            validations.append(validation)
        
        self.validations = validations
        
        print(f"✅ Market Validator Agent: Completed {len(validations)} validations")
        
        return validations
    
    async def _create_campaign(
        self,
        idea: BusinessIdea,
        budget: float,
        duration_days: int
    ) -> AdCampaign:
        """
        Create an ad campaign for an idea.
        
        In production, this would:
        1. Generate compelling ad copy using LLM
        2. Create landing page
        3. Set up conversion tracking
        4. Configure targeting
        5. Launch campaign via Meta/Google Ads API
        """
        print(f"  📢 Creating campaign for: {idea.title}")
        await asyncio.sleep(0.3)
        
        # Generate ad copy (in production, use LLM)
        ad_copy = self._generate_ad_copy(idea)
        
        # Determine platform based on target market
        platform = self._select_platform(idea)
        
        campaign = AdCampaign(
            id=f"campaign_{idea.id[:8]}",
            idea_id=idea.id,
            platform=platform,
            campaign_name=f"Validation: {idea.title}",
            ad_copy=ad_copy,
            targeting=self._generate_targeting(idea),
            budget=budget,
            duration_days=duration_days,
            status="running"
        )
        
        return campaign
    
    def _generate_ad_copy(self, idea: BusinessIdea) -> str:
        """Generate compelling ad copy"""
        # In production, use LLM to generate multiple variations
        return f"""
🚀 {idea.title}

{idea.value_proposition}

✨ Key Benefits:
{chr(10).join('• ' + feature for feature in idea.key_features[:3])}

👉 Learn More - Limited Early Access!
        """.strip()
    
    def _select_platform(self, idea: BusinessIdea) -> AdPlatform:
        """Select best ad platform based on target market"""
        # Simple heuristics - in production, use more sophisticated logic
        target = idea.target_market.lower()
        
        if "developer" in target or "software" in target or "tech" in target:
            return AdPlatform.GOOGLE  # Developers often use Google
        elif "b2b" in target or "enterprise" in target or "business" in target:
            return AdPlatform.LINKEDIN if "LINKEDIN" in str(AdPlatform.__members__) else AdPlatform.GOOGLE
        else:
            return AdPlatform.META  # Consumer-focused
    
    def _generate_targeting(self, idea: BusinessIdea) -> dict:
        """Generate targeting parameters"""
        return {
            "interests": idea.keywords if hasattr(idea, 'keywords') else [],
            "age_range": {"min": 25, "max": 55},
            "locations": ["US", "CA", "UK", "AU"],
            "device_types": ["mobile", "desktop"]
        }
    
    async def _run_and_analyze_campaign(
        self,
        campaign: AdCampaign,
        idea: BusinessIdea,
        analysis: Optional[BusinessAnalysis]
    ) -> ValidationResult:
        """
        Run campaign and analyze results.
        
        In production:
        1. Monitor campaign daily via API
        2. Collect real metrics
        3. Analyze performance
        4. Make optimization decisions
        """
        print(f"  📊 Running {campaign.duration_days}-day campaign on {campaign.platform.value}...")
        await asyncio.sleep(0.5)  # Simulate campaign running
        
        # TODO: Replace with actual API calls to Meta/Google Ads
        # For now, generate realistic mock metrics
        metrics = self._generate_mock_metrics(campaign, analysis)
        
        # Analyze results
        is_promising = self._is_idea_promising(metrics, analysis)
        confidence_level = self._calculate_confidence(metrics)
        insights = self._generate_insights(metrics, campaign)
        recommendations = self._generate_recommendations(is_promising, metrics)
        
        validation = ValidationResult(
            idea_id=idea.id,
            metrics=metrics,
            is_promising=is_promising,
            confidence_level=confidence_level,
            key_insights=insights,
            recommendations=recommendations
        )
        
        return validation
    
    def _generate_mock_metrics(
        self,
        campaign: AdCampaign,
        analysis: Optional[BusinessAnalysis]
    ) -> ValidationMetrics:
        """Generate realistic mock campaign metrics"""
        
        # Base metrics on viability score if available
        base_performance = 0.5
        if analysis:
            # Higher viability score = better campaign performance
            base_performance = (analysis.viability_score / 10.0) * 0.7 + 0.3
        
        # Randomize a bit for realism
        performance_factor = base_performance * random.uniform(0.8, 1.2)
        
        # Generate metrics
        impressions = int(random.randint(50000, 200000) * performance_factor)
        ctr = min(0.15, max(0.005, random.gauss(0.03, 0.015) * performance_factor))
        clicks = int(impressions * ctr)
        
        conversion_rate = min(0.20, max(0.01, random.gauss(0.05, 0.02) * performance_factor))
        conversions = int(clicks * conversion_rate)
        
        cost = campaign.budget
        cpc = cost / clicks if clicks > 0 else 0
        
        # Engagement score (0-10) based on overall performance
        engagement_score = (
            (ctr / 0.05) * 3 +  # CTR weight
            (conversion_rate / 0.1) * 4 +  # Conversion weight
            (min(conversions / 50, 1.0)) * 3  # Absolute conversions weight
        )
        engagement_score = min(10.0, max(0.0, engagement_score))
        
        return ValidationMetrics(
            campaign_id=campaign.id,
            impressions=impressions,
            clicks=clicks,
            conversions=conversions,
            cost=cost,
            ctr=ctr,
            cpc=cpc,
            conversion_rate=conversion_rate,
            engagement_score=engagement_score
        )
    
    def _is_idea_promising(
        self,
        metrics: ValidationMetrics,
        analysis: Optional[BusinessAnalysis]
    ) -> bool:
        """Determine if idea shows promise based on metrics"""
        
        # Thresholds for promising results
        min_ctr = 0.015  # 1.5% CTR
        min_conversion_rate = 0.02  # 2% conversion
        min_engagement_score = 5.0
        
        return (
            metrics.ctr >= min_ctr and
            metrics.conversion_rate >= min_conversion_rate and
            metrics.engagement_score >= min_engagement_score
        )
    
    def _calculate_confidence(self, metrics: ValidationMetrics) -> str:
        """Calculate confidence level in validation results"""
        
        # Based on sample size and consistency
        if metrics.conversions >= 50 and metrics.clicks >= 500:
            return "high"
        elif metrics.conversions >= 20 and metrics.clicks >= 200:
            return "medium"
        else:
            return "low"
    
    def _generate_insights(self, metrics: ValidationMetrics, campaign: AdCampaign) -> List[str]:
        """Generate insights from campaign data"""
        
        insights = []
        
        # CTR insights
        if metrics.ctr > 0.04:
            insights.append(f"Strong CTR of {metrics.ctr*100:.2f}% indicates compelling value proposition")
        elif metrics.ctr < 0.01:
            insights.append(f"Low CTR of {metrics.ctr*100:.2f}% suggests messaging needs improvement")
        
        # Conversion insights
        if metrics.conversion_rate > 0.08:
            insights.append(f"High conversion rate of {metrics.conversion_rate*100:.1f}% shows strong market interest")
        elif metrics.conversion_rate < 0.03:
            insights.append(f"Low conversion rate may indicate landing page or offer needs optimization")
        
        # Cost insights
        if metrics.cpc < 1.0:
            insights.append(f"Low CPC of ${metrics.cpc:.2f} suggests efficient targeting")
        elif metrics.cpc > 5.0:
            insights.append(f"High CPC of ${metrics.cpc:.2f} may impact profitability")
        
        # Platform insights
        insights.append(f"{campaign.platform.value.title()} platform showed engagement score of {metrics.engagement_score:.1f}/10")
        
        return insights
    
    def _generate_recommendations(self, is_promising: bool, metrics: ValidationMetrics) -> List[str]:
        """Generate actionable recommendations"""
        
        if is_promising:
            return [
                "✅ Proceed with MVP development - validation shows clear market interest",
                "Scale ad spend gradually to acquire early users",
                "A/B test different messaging to optimize conversion rate",
                "Set up email nurture campaign for leads",
                "Consider expanding to additional ad platforms"
            ]
        else:
            recommendations = ["⚠️ Results inconclusive - consider pivot or iteration"]
            
            if metrics.ctr < 0.015:
                recommendations.append("Improve ad copy and creative to increase CTR")
            
            if metrics.conversion_rate < 0.03:
                recommendations.append("Redesign landing page to better communicate value")
            
            recommendations.extend([
                "Conduct user interviews to understand hesitation",
                "Test alternative value propositions",
                "Consider narrowing or broadening target market"
            ])
            
            return recommendations
    
    def get_promising_ideas(self) -> List[ValidationResult]:
        """Get validations that show promise"""
        return [v for v in self.validations if v.is_promising]


async def main():
    """Test the Market Validator Agent"""
    from .web_scanner import WebScannerAgent
    from .idea_generator import IdeaGeneratorAgent
    from .analyst import BusinessAnalystAgent
    
    # Run full pipeline
    scanner = WebScannerAgent()
    trends = await scanner.scan_all_sources()
    
    generator = IdeaGeneratorAgent()
    ideas = await generator.generate_ideas(trends, max_ideas=3)
    
    analyst = BusinessAnalystAgent()
    analyses = await analyst.analyze_ideas(ideas)
    
    # Validate top ideas
    validator = MarketValidatorAgent()
    validations = await validator.validate_ideas(
        ideas=ideas,
        analyses=analyses,
        budget_per_idea=500.0,
        duration_days=7
    )
    
    print("\n" + "="*60)
    print("Market Validation Results:")
    print("="*60)
    
    for validation in validations:
        idea = next(i for i in ideas if i.id == validation.idea_id)
        
        status = "✅ PROMISING" if validation.is_promising else "⚠️ NEEDS WORK"
        
        print(f"\n{status}: {idea.title}")
        print(f"  Confidence: {validation.confidence_level.upper()}")
        
        m = validation.metrics
        print(f"\n  Campaign Metrics:")
        print(f"    Impressions: {m.impressions:,}")
        print(f"    Clicks: {m.clicks:,} (CTR: {m.ctr*100:.2f}%)")
        print(f"    Conversions: {m.conversions:,} (Rate: {m.conversion_rate*100:.2f}%)")
        print(f"    CPC: ${m.cpc:.2f}")
        print(f"    Engagement Score: {m.engagement_score:.1f}/10")
        
        print(f"\n  Key Insights:")
        for insight in validation.key_insights[:2]:
            print(f"    • {insight}")
        
        print(f"\n  Top Recommendation:")
        print(f"    • {validation.recommendations[0]}")
    
    # Summary
    promising_count = len(validator.get_promising_ideas())
    print(f"\n{'='*60}")
    print(f"Summary: {promising_count}/{len(validations)} ideas show promise")
    print(f"{'='*60}")


if __name__ == "__main__":
    asyncio.run(main())
