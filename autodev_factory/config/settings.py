"""
Configuration Settings for AutoDev Factory

This module defines all configuration settings using Pydantic.
"""

from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Optional, List
from pathlib import Path


class Settings(BaseSettings):
    """Main configuration class for AutoDev Factory."""
    
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore"
    )
    
    # AI Model APIs
    openai_api_key: str = ""
    anthropic_api_key: str = ""
    
    # GitHub Configuration
    github_token: str = ""
    github_username: str = ""
    
    # Database Configuration
    database_url: str = "sqlite:///./autodev.db"
    redis_url: str = "redis://localhost:6379"
    
    # Vector Database
    chroma_db_path: str = "./chroma_db"
    
    # Deployment Services
    vercel_token: str = ""
    aws_access_key_id: str = ""
    aws_secret_access_key: str = ""
    aws_region: str = "us-east-1"
    
    # Application Settings
    log_level: str = "INFO"
    environment: str = "development"
    max_retries: int = 3
    timeout_seconds: int = 300
    
    # Agent Settings
    default_model: str = "gpt-4-turbo-preview"
    temperature: float = 0.7
    max_tokens: int = 4096
    
    # Trend Research Sources
    trend_sources: List[str] = [
        "google_trends",
        "product_hunt",
        "reddit",
        "hackernews",
        "github_trending",
        "twitter"
    ]
    
    # Supported Niches
    supported_niches: List[str] = [
        "seo_tools",
        "shopify_automation",
        "youtube_automation",
        "ai_content_tools",
        "chrome_extensions",
        "marketing_automation",
        "saas_micro_tools",
        "developer_tools",
        "productivity_tools",
        "analytics_tools"
    ]
    
    # Supported Tech Stacks
    supported_stacks: List[str] = [
        "nextjs_fastapi",
        "react_express",
        "vue_django",
        "svelte_fastapi",
        "plain_python",
        "node_only"
    ]
    
    # Output Directory
    output_dir: Path = Path("./output")
    
    # Templates Directory
    templates_dir: Path = Path("./templates")
    
    @property
    def is_production(self) -> bool:
        """Check if running in production environment."""
        return self.environment == "production"
    
    @property
    def has_openai_key(self) -> bool:
        """Check if OpenAI API key is configured."""
        return bool(self.openai_api_key) and self.openai_api_key != "your_openai_key_here"
    
    @property
    def has_anthropic_key(self) -> bool:
        """Check if Anthropic API key is configured."""
        return bool(self.anthropic_api_key) and self.anthropic_api_key != "your_anthropic_key_here"
    
    @property
    def has_github_token(self) -> bool:
        """Check if GitHub token is configured."""
        return bool(self.github_token) and self.github_token != "your_github_token_here"
    
    def validate_configuration(self) -> List[str]:
        """
        Validate the configuration and return a list of warnings.
        
        Returns:
            List of warning messages for missing or invalid configurations.
        """
        warnings = []
        
        if not self.has_openai_key and not self.has_anthropic_key:
            warnings.append(
                "No AI model API key configured. Please set OPENAI_API_KEY or ANTHROPIC_API_KEY"
            )
        
        if not self.has_github_token:
            warnings.append(
                "GitHub token not configured. GitHub integration will be limited."
            )
        
        if self.environment == "production" and self.log_level == "DEBUG":
            warnings.append(
                "Log level is set to DEBUG in production. Consider changing to INFO or WARNING."
            )
        
        return warnings


# Global settings instance
_settings: Optional[Settings] = None


def get_settings() -> Settings:
    """
    Get or create the global settings instance.
    
    Returns:
        Settings instance with loaded configuration.
    """
    global _settings
    if _settings is None:
        _settings = Settings()
    return _settings


def reload_settings() -> Settings:
    """
    Reload settings from environment variables.
    
    Returns:
        New Settings instance with refreshed configuration.
    """
    global _settings
    _settings = Settings()
    return _settings
