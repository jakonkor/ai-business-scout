"""
AI Business Scout - Data Models and Schemas
"""

from datetime import datetime
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field
from enum import Enum


class TrendSource(str, Enum):
    """Source of the trend data"""
    TWITTER = "twitter"
    REDDIT = "reddit"
    NEWS = "news"
    GOOGLE_TRENDS = "google_trends"
    OTHER = "other"


class Trend(BaseModel):
    """A detected trend or signal from web sources"""
    id: str
    source: TrendSource
    title: str
    description: str
    url: Optional[str] = None
    sentiment: float = Field(ge=-1.0, le=1.0, description="Sentiment score from -1 to 1")
    engagement: int = Field(ge=0, description="Likes, shares, upvotes, etc.")
    keywords: List[str] = []
    timestamp: datetime = Field(default_factory=datetime.now)
    raw_data: Dict[str, Any] = {}


class BusinessIdea(BaseModel):
    """A generated business idea"""
    id: str
    title: str
    description: str
    value_proposition: str
    target_market: str
    problem_solved: str
    revenue_model: str
    estimated_market_size: Optional[str] = None
    key_features: List[str] = []
    source_trends: List[str] = Field(description="IDs of trends that inspired this idea")
    generated_at: datetime = Field(default_factory=datetime.now)


class AnalysisType(str, Enum):
    """Type of business analysis"""
    SWOT = "swot"
    PORTER_FIVE_FORCES = "porter_five_forces"
    MARKET_SIZING = "market_sizing"
    COMPETITIVE = "competitive"


class SWOTAnalysis(BaseModel):
    """SWOT Analysis results"""
    strengths: List[str]
    weaknesses: List[str]
    opportunities: List[str]
    threats: List[str]


class BusinessAnalysis(BaseModel):
    """Strategic analysis of a business idea"""
    idea_id: str
    swot: SWOTAnalysis
    competitive_landscape: str
    market_size_estimate: str
    revenue_potential: str
    risk_level: str = Field(description="low, medium, high")
    viability_score: float = Field(ge=0.0, le=10.0, description="Score from 0-10")
    key_assumptions: List[str] = []
    recommended_next_steps: List[str] = []
    analyzed_at: datetime = Field(default_factory=datetime.now)


class AdPlatform(str, Enum):
    """Ad platform for validation"""
    META = "meta"
    GOOGLE = "google"
    LINKEDIN = "linkedin"


class AdCampaign(BaseModel):
    """Ad campaign for market validation"""
    id: str
    idea_id: str
    platform: AdPlatform
    campaign_name: str
    ad_copy: str
    targeting: Dict[str, Any]
    budget: float
    duration_days: int
    status: str = "draft"
    created_at: datetime = Field(default_factory=datetime.now)


class ValidationMetrics(BaseModel):
    """Metrics from market validation campaign"""
    campaign_id: str
    impressions: int = 0
    clicks: int = 0
    conversions: int = 0
    cost: float = 0.0
    ctr: float = Field(ge=0.0, le=1.0, description="Click-through rate")
    cpc: float = Field(ge=0.0, description="Cost per click")
    conversion_rate: float = Field(ge=0.0, le=1.0)
    engagement_score: float = Field(ge=0.0, le=10.0, description="Overall engagement score")
    validated_at: datetime = Field(default_factory=datetime.now)


class ValidationResult(BaseModel):
    """Final validation result for a business idea"""
    idea_id: str
    metrics: ValidationMetrics
    is_promising: bool
    confidence_level: str = Field(description="low, medium, high")
    key_insights: List[str] = []
    recommendations: List[str] = []
    validated_at: datetime = Field(default_factory=datetime.now)


class ScoutReport(BaseModel):
    """Complete report from the business scout pipeline"""
    trends_found: List[Trend]
    ideas_generated: List[BusinessIdea]
    analyses: List[BusinessAnalysis]
    validations: List[ValidationResult]
    top_recommendations: List[str]
    generated_at: datetime = Field(default_factory=datetime.now)
