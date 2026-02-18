"""
Configuration management for AI Business Scout
"""

import os
from pathlib import Path
from typing import Optional
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Project paths
PROJECT_ROOT = Path(__file__).parent.parent.parent
DATA_DIR = PROJECT_ROOT / "data"
CONFIG_DIR = PROJECT_ROOT / "config"

# Ensure directories exist
DATA_DIR.mkdir(exist_ok=True)
CONFIG_DIR.mkdir(exist_ok=True)


class Config:
    """Application configuration"""
    
    # AI Provider API Keys
    OPENAI_API_KEY: Optional[str] = os.getenv("OPENAI_API_KEY")
    ANTHROPIC_API_KEY: Optional[str] = os.getenv("ANTHROPIC_API_KEY")
    
    # Twitter/X API
    TWITTER_API_KEY: Optional[str] = os.getenv("TWITTER_API_KEY")
    TWITTER_API_SECRET: Optional[str] = os.getenv("TWITTER_API_SECRET")
    TWITTER_ACCESS_TOKEN: Optional[str] = os.getenv("TWITTER_ACCESS_TOKEN")
    TWITTER_ACCESS_SECRET: Optional[str] = os.getenv("TWITTER_ACCESS_SECRET")
    TWITTER_BEARER_TOKEN: Optional[str] = os.getenv("TWITTER_BEARER_TOKEN")
    
    # Reddit API
    REDDIT_CLIENT_ID: Optional[str] = os.getenv("REDDIT_CLIENT_ID")
    REDDIT_CLIENT_SECRET: Optional[str] = os.getenv("REDDIT_CLIENT_SECRET")
    REDDIT_USER_AGENT: str = os.getenv("REDDIT_USER_AGENT", "ai-business-scout/1.0")
    
    # Meta Ads API
    META_ACCESS_TOKEN: Optional[str] = os.getenv("META_ACCESS_TOKEN")
    META_AD_ACCOUNT_ID: Optional[str] = os.getenv("META_AD_ACCOUNT_ID")
    META_APP_ID: Optional[str] = os.getenv("META_APP_ID")
    META_APP_SECRET: Optional[str] = os.getenv("META_APP_SECRET")
    
    # Google Ads API
    GOOGLE_ADS_DEVELOPER_TOKEN: Optional[str] = os.getenv("GOOGLE_ADS_DEVELOPER_TOKEN")
    GOOGLE_ADS_CLIENT_ID: Optional[str] = os.getenv("GOOGLE_ADS_CLIENT_ID")
    GOOGLE_ADS_CLIENT_SECRET: Optional[str] = os.getenv("GOOGLE_ADS_CLIENT_SECRET")
    GOOGLE_ADS_REFRESH_TOKEN: Optional[str] = os.getenv("GOOGLE_ADS_REFRESH_TOKEN")
    GOOGLE_ADS_CUSTOMER_ID: Optional[str] = os.getenv("GOOGLE_ADS_CUSTOMER_ID")
    
    # News API
    NEWS_API_KEY: Optional[str] = os.getenv("NEWS_API_KEY")
    
    # Slack integration
    SLACK_WEBHOOK_URL: Optional[str] = os.getenv("SLACK_WEBHOOK_URL")
    
    # Database
    DATABASE_URL: str = os.getenv("DATABASE_URL", f"sqlite:///{DATA_DIR}/business_scout.db")
    
    # Application settings
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")
    SCAN_INTERVAL_HOURS: int = int(os.getenv("SCAN_INTERVAL_HOURS", "24"))
    MAX_IDEAS_PER_RUN: int = int(os.getenv("MAX_IDEAS_PER_RUN", "10"))
    
    # Scheduler settings (used by scripts/setup_cron.sh)
    # Cron expression for the daily run, e.g. "0 8 * * *" = every day at 08:00
    SCHEDULE_CRON: str = os.getenv("SCHEDULE_CRON", "0 8 * * *")
    
    @classmethod
    def validate(cls) -> bool:
        """Validate that required configuration is present"""
        errors = []
        
        # Check AI provider (at least one required)
        if not cls.OPENAI_API_KEY and not cls.ANTHROPIC_API_KEY:
            errors.append("Either OPENAI_API_KEY or ANTHROPIC_API_KEY must be set")
        
        if errors:
            print("Configuration errors:")
            for error in errors:
                print(f"  - {error}")
            return False
        
        return True
    
    @classmethod
    def get_ai_provider(cls) -> str:
        """Get the configured AI provider"""
        if cls.OPENAI_API_KEY:
            return "openai"
        elif cls.ANTHROPIC_API_KEY:
            return "anthropic"
        else:
            raise ValueError("No AI provider configured")


# Create a singleton instance
config = Config()
