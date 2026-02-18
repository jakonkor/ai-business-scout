"""
Slack Notifier - Posts pipeline progress and results to a Slack channel
via an Incoming Webhook URL.
"""

import json
import logging
from datetime import datetime
from typing import List, Optional

import requests

from ..models import BusinessIdea, BusinessAnalysis, ValidationResult, ScoutReport

logger = logging.getLogger(__name__)


class SlackNotifier:
    """
    Posts notifications to Slack using an Incoming Webhook.

    Configure the webhook URL in .env:
        SLACK_WEBHOOK_URL=https://hooks.slack.com/services/XXX/YYY/ZZZ

    Obtain a webhook at: https://api.slack.com/messaging/webhooks
    """

    def __init__(self, webhook_url: Optional[str] = None):
        from .config import config  # local import to avoid circular dependency
        self.webhook_url = webhook_url or config.SLACK_WEBHOOK_URL
        self.enabled = bool(self.webhook_url)
        if not self.enabled:
            logger.debug("Slack notifications disabled: SLACK_WEBHOOK_URL not set.")

    # ------------------------------------------------------------------
    # Public helpers called from the main pipeline
    # ------------------------------------------------------------------

    def notify_pipeline_start(self) -> None:
        """Notify that a new pipeline run has started."""
        if not self.enabled:
            return
        self._post({
            "text": ":rocket: *AI Business Scout pipeline started*",
            "attachments": [
                {
                    "color": "#36a64f",
                    "text": f"Run started at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
                }
            ],
        })

    def notify_phase(self, phase_number: int, phase_name: str, detail: str = "") -> None:
        """Notify the start of a pipeline phase."""
        if not self.enabled:
            return
        icons = {1: ":mag:", 2: ":bulb:", 3: ":bar_chart:", 4: ":dart:"}
        icon = icons.get(phase_number, ":white_circle:")
        text = f"{icon} *Phase {phase_number}: {phase_name}*"
        if detail:
            text += f"\n{detail}"
        self._post({"text": text})

    def notify_report(self, report: ScoutReport, top_n: int = 3) -> None:
        """
        Post a rich summary of the scout report to Slack.
        Includes top ideas with their scores and key recommendations.

        Args:
            report: The completed scout report.
            top_n: Number of top ideas to include in the Slack message.
        """
        if not self.enabled:
            return

        promising = [v for v in report.validations if v.is_promising]
        total = len(report.validations)

        header = (
            f":memo: *AI Business Scout — Run Complete*\n"
            f"Trends: *{len(report.trends_found)}* | "
            f"Ideas: *{len(report.ideas_generated)}* | "
            f"Promising: *{len(promising)}/{total}*"
        )

        attachments = []

        # Top recommendations
        if report.top_recommendations:
            attachments.append({
                "color": "#2eb886",
                "title": ":trophy: Top Recommendations",
                "text": "\n".join(report.top_recommendations),
                "mrkdwn_in": ["text"],
            })

        # Build lookup dicts to avoid O(n²) searches inside the loop
        ideas_by_id = {i.id: i for i in report.ideas_generated}
        analyses_by_id = {a.idea_id: a for a in report.analyses}

        # Top ideas sorted by engagement score
        sorted_validations = sorted(
            report.validations,
            key=lambda v: v.metrics.engagement_score,
            reverse=True,
        )[:top_n]

        for rank, validation in enumerate(sorted_validations, start=1):
            idea = ideas_by_id.get(validation.idea_id)
            analysis = analyses_by_id.get(validation.idea_id)
            if not idea:
                continue

            status_icon = ":white_check_mark:" if validation.is_promising else ":warning:"
            viability = f"{analysis.viability_score:.1f}/10" if analysis else "N/A"

            attachments.append({
                "color": "#36a64f" if validation.is_promising else "#ff9900",
                "title": f"{status_icon} #{rank}: {idea.title}",
                "fields": [
                    {
                        "title": "Value Proposition",
                        "value": idea.value_proposition,
                        "short": False,
                    },
                    {
                        "title": "Viability Score",
                        "value": viability,
                        "short": True,
                    },
                    {
                        "title": "Engagement Score",
                        "value": f"{validation.metrics.engagement_score:.1f}/10",
                        "short": True,
                    },
                    {
                        "title": "CTR",
                        "value": f"{validation.metrics.ctr * 100:.2f}%",
                        "short": True,
                    },
                    {
                        "title": "Conversions",
                        "value": str(validation.metrics.conversions),
                        "short": True,
                    },
                ],
                "footer": f"Confidence: {validation.confidence_level.upper()} | "
                          f"Revenue model: {idea.revenue_model}",
                "mrkdwn_in": ["text", "fields"],
            })

        self._post({"text": header, "attachments": attachments})

    def notify_error(self, message: str) -> None:
        """Post an error notification."""
        if not self.enabled:
            return
        self._post({
            "text": f":x: *AI Business Scout error*\n{message}",
            "attachments": [{"color": "#cc0000", "text": message}],
        })

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    def _post(self, payload: dict) -> bool:
        """
        POST a JSON payload to the Slack webhook URL.

        Returns:
            True on success, False on failure (non-raising).
        """
        if not self.webhook_url:
            return False
        try:
            response = requests.post(
                self.webhook_url,
                data=json.dumps(payload),
                headers={"Content-Type": "application/json"},
                timeout=10,
            )
            if response.status_code != 200:
                logger.warning(
                    "Slack notification failed: %s %s",
                    response.status_code,
                    response.text,
                )
                return False
            return True
        except requests.RequestException as exc:
            logger.warning("Slack notification error: %s", exc)
            return False
