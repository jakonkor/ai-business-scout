#!/usr/bin/env python3
"""
AI Business Scout — Scheduler Entry Point
==========================================
This script is designed to be invoked by cron (or any other job scheduler).
It runs the full business-scouting pipeline and writes a timestamped log file
to the ``logs/`` directory so you have a permanent record of every run.

Typical cron usage (edit with ``crontab -e``):
    # Run every day at 08:00
    0 8 * * * /path/to/venv/bin/python /path/to/ai-business-scout/scheduler.py >> /path/to/ai-business-scout/logs/cron.log 2>&1

Alternatively, use the helper script to install/remove the cron entry:
    bash scripts/setup_cron.sh install
    bash scripts/setup_cron.sh remove
"""

import asyncio
import logging
import sys
from datetime import datetime
from pathlib import Path

# ---------------------------------------------------------------------------
# Ensure the project root is on sys.path so that ``import src`` works when
# this script is called directly by cron (without activating the venv or
# changing the working directory).
# ---------------------------------------------------------------------------
PROJECT_ROOT = Path(__file__).resolve().parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

# ---------------------------------------------------------------------------
# Logging — write to logs/ directory so cron output is preserved.
# ---------------------------------------------------------------------------
LOGS_DIR = PROJECT_ROOT / "logs"
LOGS_DIR.mkdir(exist_ok=True)

log_filename = LOGS_DIR / f"scout_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s — %(message)s",
    handlers=[
        logging.FileHandler(log_filename),
        logging.StreamHandler(sys.stdout),
    ],
)
logger = logging.getLogger("scheduler")


async def run() -> int:
    """
    Execute the full scouting pipeline.

    Returns:
        Exit code — 0 on success, 1 on failure.
    """
    from src.utils.config import Config
    from src.main import BusinessScout

    logger.info("AI Business Scout — scheduled run starting")

    if not Config.validate():
        logger.error("Configuration incomplete. Check your .env file.")
        return 1

    try:
        scout = BusinessScout()
        report = await scout.run_full_pipeline(
            max_ideas=Config.MAX_IDEAS_PER_RUN,
            validation_budget_per_idea=500.0,
            validation_duration_days=7,
        )
        if report is None:
            logger.warning("Pipeline returned no report (no trends found).")
            return 1

        logger.info(
            "Pipeline complete — %d trends, %d ideas, %d validations.",
            len(report.trends_found),
            len(report.ideas_generated),
            len(report.validations),
        )
        return 0

    except Exception as exc:  # noqa: BLE001
        logger.exception(
            "Unhandled %s during pipeline run: %s",
            type(exc).__name__,
            exc,
        )
        return 1


if __name__ == "__main__":
    exit_code = asyncio.run(run())
    sys.exit(exit_code)
