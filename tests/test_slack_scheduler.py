"""
Tests for Slack notifier and scheduler entry point.
"""

import json
from unittest.mock import MagicMock, patch

import pytest

from src.utils.slack_notifier import SlackNotifier


# ---------------------------------------------------------------------------
# SlackNotifier — disabled when no webhook URL is configured
# ---------------------------------------------------------------------------

class TestSlackNotifierDisabled:
    """When SLACK_WEBHOOK_URL is not set the notifier is a no-op."""

    def setup_method(self):
        self.notifier = SlackNotifier(webhook_url=None)

    def test_notifier_is_disabled(self):
        assert not self.notifier.enabled

    def test_notify_pipeline_start_does_not_post(self):
        with patch.object(self.notifier, "_post") as mock_post:
            self.notifier.notify_pipeline_start()
            mock_post.assert_not_called()

    def test_notify_phase_does_not_post(self):
        with patch.object(self.notifier, "_post") as mock_post:
            self.notifier.notify_phase(1, "Web Scanning")
            mock_post.assert_not_called()

    def test_notify_error_does_not_post(self):
        with patch.object(self.notifier, "_post") as mock_post:
            self.notifier.notify_error("Something went wrong")
            mock_post.assert_not_called()


# ---------------------------------------------------------------------------
# SlackNotifier — enabled (webhook URL is set)
# ---------------------------------------------------------------------------

class TestSlackNotifierEnabled:
    """When a webhook URL is set the notifier calls requests.post."""

    FAKE_URL = "https://hooks.slack.com/services/FAKE/FAKE/FAKE"

    def setup_method(self):
        self.notifier = SlackNotifier(webhook_url=self.FAKE_URL)

    def test_notifier_is_enabled(self):
        assert self.notifier.enabled

    def test_notify_pipeline_start_posts(self):
        mock_resp = MagicMock()
        mock_resp.status_code = 200
        with patch("requests.post", return_value=mock_resp) as mock_post:
            self.notifier.notify_pipeline_start()
            mock_post.assert_called_once()
            _, kwargs = mock_post.call_args
            assert kwargs["headers"]["Content-Type"] == "application/json"
            payload = json.loads(kwargs["data"])
            assert "text" in payload

    def test_notify_phase_posts_correct_phase_number(self):
        mock_resp = MagicMock()
        mock_resp.status_code = 200
        with patch("requests.post", return_value=mock_resp) as mock_post:
            self.notifier.notify_phase(2, "Idea Generation", "detail")
            mock_post.assert_called_once()
            payload = json.loads(mock_post.call_args[1]["data"])
            assert "Phase 2" in payload["text"]
            assert "Idea Generation" in payload["text"]

    def test_notify_error_posts(self):
        mock_resp = MagicMock()
        mock_resp.status_code = 200
        with patch("requests.post", return_value=mock_resp) as mock_post:
            self.notifier.notify_error("boom")
            mock_post.assert_called_once()
            payload = json.loads(mock_post.call_args[1]["data"])
            assert "boom" in payload["text"]

    def test_http_failure_does_not_raise(self):
        """A non-200 response should log a warning but not raise."""
        mock_resp = MagicMock()
        mock_resp.status_code = 500
        mock_resp.text = "Internal Server Error"
        with patch("requests.post", return_value=mock_resp):
            # Should not raise
            self.notifier.notify_pipeline_start()

    def test_network_error_does_not_raise(self):
        """A network error should log a warning but not raise."""
        import requests as req
        with patch("requests.post", side_effect=req.RequestException("timeout")):
            self.notifier.notify_pipeline_start()

    def test_notify_report_posts(self):
        """notify_report should post a Slack message with top ideas."""
        from datetime import datetime
        from src.models import (
            ScoutReport, Trend, TrendSource, BusinessIdea,
            BusinessAnalysis, SWOTAnalysis, ValidationResult,
            ValidationMetrics,
        )

        trend = Trend(
            id="t1", source=TrendSource.TWITTER,
            title="AI Trend", description="desc",
            sentiment=0.8, engagement=5000, keywords=["AI"],
        )
        idea = BusinessIdea(
            id="i1", title="AI Tool", description="desc",
            value_proposition="VP", target_market="devs",
            problem_solved="problem", revenue_model="SaaS",
            source_trends=["t1"],
        )
        swot = SWOTAnalysis(
            strengths=["s1"], weaknesses=["w1"],
            opportunities=["o1"], threats=["t1"],
        )
        analysis = BusinessAnalysis(
            idea_id="i1", swot=swot,
            competitive_landscape="low competition",
            market_size_estimate="TAM $1B",
            revenue_potential="$1M ARR",
            risk_level="low", viability_score=8.0,
        )
        metrics = ValidationMetrics(
            campaign_id="c1", impressions=100000, clicks=3000,
            conversions=150, cost=500.0, ctr=0.03,
            cpc=0.17, conversion_rate=0.05, engagement_score=7.5,
        )
        validation = ValidationResult(
            idea_id="i1", metrics=metrics, is_promising=True,
            confidence_level="high",
        )
        report = ScoutReport(
            trends_found=[trend],
            ideas_generated=[idea],
            analyses=[analysis],
            validations=[validation],
            top_recommendations=["Launch MVP now"],
        )

        mock_resp = MagicMock()
        mock_resp.status_code = 200
        with patch("requests.post", return_value=mock_resp) as mock_post:
            self.notifier.notify_report(report)
            mock_post.assert_called_once()
            payload = json.loads(mock_post.call_args[1]["data"])
            assert "AI Tool" in str(payload)
            assert "Launch MVP now" in str(payload)
