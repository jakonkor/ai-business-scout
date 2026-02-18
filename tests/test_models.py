"""
Tests for AI Business Scout
"""

import pytest
from src.models import Trend, TrendSource, BusinessIdea


def test_trend_creation():
    """Test creating a trend"""
    trend = Trend(
        id="test-1",
        source=TrendSource.TWITTER,
        title="Test Trend",
        description="A test trend",
        sentiment=0.5,
        engagement=1000,
        keywords=["test", "trending"]
    )
    
    assert trend.id == "test-1"
    assert trend.source == TrendSource.TWITTER
    assert trend.sentiment == 0.5


def test_business_idea_creation():
    """Test creating a business idea"""
    idea = BusinessIdea(
        id="idea-1",
        title="Test Idea",
        description="A test business idea",
        value_proposition="Solve a problem",
        target_market="Developers",
        problem_solved="Lack of testing",
        revenue_model="SaaS",
        source_trends=["trend-1"]
    )
    
    assert idea.id == "idea-1"
    assert idea.title == "Test Idea"
    assert len(idea.source_trends) == 1


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
