#!/usr/bin/env bash
# =============================================================================
# AI Business Scout — Cron Setup Helper
# =============================================================================
# Usage:
#   bash scripts/setup_cron.sh install   # Install (or update) the cron job
#   bash scripts/setup_cron.sh remove    # Remove the cron job
#   bash scripts/setup_cron.sh status    # Show current cron entry (if any)
#
# The cron schedule is read from the SCHEDULE_CRON variable in the .env file,
# falling back to "0 8 * * *" (every day at 08:00 local time).
#
# Environment variables (can be set in .env):
#   SCHEDULE_CRON   — Standard cron expression (default: "0 8 * * *")
# =============================================================================

set -euo pipefail

# ---------------------------------------------------------------------------
# Resolve project root (directory that contains this script's parent)
# ---------------------------------------------------------------------------
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"

# ---------------------------------------------------------------------------
# Load .env if present so SCHEDULE_CRON can be overridden there
# ---------------------------------------------------------------------------
ENV_FILE="${PROJECT_ROOT}/.env"
if [[ -f "${ENV_FILE}" ]]; then
    # Export only the SCHEDULE_CRON variable; ignore errors for other lines
    set +e
    SCHEDULE_CRON_FROM_ENV=$(grep -E '^SCHEDULE_CRON=' "${ENV_FILE}" | head -1 | cut -d= -f2-)
    set -e
fi

SCHEDULE_CRON="${SCHEDULE_CRON_FROM_ENV:-${SCHEDULE_CRON:-0 8 * * *}}"

# ---------------------------------------------------------------------------
# Detect Python interpreter (prefer the active venv, fall back to python3)
# ---------------------------------------------------------------------------
if [[ -n "${VIRTUAL_ENV:-}" ]]; then
    PYTHON="${VIRTUAL_ENV}/bin/python"
elif [[ -f "${PROJECT_ROOT}/venv/bin/python" ]]; then
    PYTHON="${PROJECT_ROOT}/venv/bin/python"
elif [[ -f "${PROJECT_ROOT}/.venv/bin/python" ]]; then
    PYTHON="${PROJECT_ROOT}/.venv/bin/python"
else
    PYTHON="$(command -v python3 || command -v python)"
fi

SCHEDULER_SCRIPT="${PROJECT_ROOT}/scheduler.py"
CRON_LOG="${PROJECT_ROOT}/logs/cron.log"
CRON_CMD="${PYTHON} ${SCHEDULER_SCRIPT} >> ${CRON_LOG} 2>&1"
CRON_ENTRY="${SCHEDULE_CRON} ${CRON_CMD}"

# Unique marker so we can find/replace this entry later
CRON_MARKER="# ai-business-scout"
CRON_LINE="${CRON_ENTRY} ${CRON_MARKER}"

# ---------------------------------------------------------------------------
# Helper functions
# ---------------------------------------------------------------------------

cron_install() {
    echo "Installing cron job..."
    echo "  Schedule : ${SCHEDULE_CRON}"
    echo "  Python   : ${PYTHON}"
    echo "  Script   : ${SCHEDULER_SCRIPT}"
    echo "  Log      : ${CRON_LOG}"
    echo ""

    # Ensure the logs directory exists
    mkdir -p "$(dirname "${CRON_LOG}")"

    # Read existing crontab (ignore error if empty)
    EXISTING_CRON=$(crontab -l 2>/dev/null || true)

    # Remove any previous ai-business-scout entry
    CLEANED_CRON=$(echo "${EXISTING_CRON}" | grep -v "${CRON_MARKER}" || true)

    # Append the new entry
    NEW_CRON="${CLEANED_CRON}
${CRON_LINE}"

    echo "${NEW_CRON}" | crontab -
    echo "✅ Cron job installed. Run 'crontab -l' to verify."
}

cron_remove() {
    echo "Removing cron job..."
    EXISTING_CRON=$(crontab -l 2>/dev/null || true)
    if echo "${EXISTING_CRON}" | grep -q "${CRON_MARKER}"; then
        CLEANED_CRON=$(echo "${EXISTING_CRON}" | grep -v "${CRON_MARKER}" || true)
        echo "${CLEANED_CRON}" | crontab -
        echo "✅ Cron job removed."
    else
        echo "ℹ️  No ai-business-scout cron entry found."
    fi
}

cron_status() {
    EXISTING_CRON=$(crontab -l 2>/dev/null || true)
    ENTRY=$(echo "${EXISTING_CRON}" | grep "${CRON_MARKER}" || true)
    if [[ -n "${ENTRY}" ]]; then
        echo "✅ Cron job is installed:"
        echo "  ${ENTRY}"
    else
        echo "❌ No ai-business-scout cron entry found."
    fi
}

# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------
ACTION="${1:-}"

case "${ACTION}" in
    install)  cron_install ;;
    remove)   cron_remove  ;;
    status)   cron_status  ;;
    *)
        echo "Usage: bash scripts/setup_cron.sh {install|remove|status}"
        exit 1
        ;;
esac
