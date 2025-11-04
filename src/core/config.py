"""
Configuration management for SCM NLP Workflow.

Handles environment variable validation and configuration loading.
"""

import os
from typing import Optional

from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


class ConfigError(Exception):
    """Raised when required configuration is missing or invalid."""

    pass


def validate_environment() -> None:
    """
    Validate that all required environment variables are set.

    Checks for required SCM credentials and raises ConfigError if any are missing.

    Raises:
        ConfigError: If any required environment variables are not set

    Example:
        >>> validate_environment()  # Raises if env vars missing
    """
    required_vars = [
        "SCM_CLIENT_ID",
        "SCM_CLIENT_SECRET",
        "SCM_TSG_ID",
        "ANTHROPIC_API_KEY",
    ]
    missing_vars = [var for var in required_vars if not os.getenv(var)]

    if missing_vars:
        raise ConfigError(
            f"Missing required environment variables: {', '.join(missing_vars)}\n"
            f"Please set them in your .env file or environment."
        )


def get_config(
    key: str, default: Optional[str] = None, required: bool = False
) -> Optional[str]:
    """
    Get configuration value from environment.

    Args:
        key: Environment variable name
        default: Default value if not set (default: None)
        required: Whether this config is required (raises if missing)

    Returns:
        Configuration value or default

    Raises:
        ConfigError: If required=True and key is not set

    Example:
        >>> api_key = get_config("ANTHROPIC_API_KEY", required=True)
        >>> project = get_config("LANGCHAIN_PROJECT", default="default-project")
    """
    value = os.getenv(key, default)

    if required and not value:
        raise ConfigError(f"Required configuration '{key}' is not set")

    return value


def get_scm_credentials() -> dict[str, str]:
    """
    Get SCM credentials from environment.

    Returns:
        Dictionary with SCM credentials (client_id, client_secret, tsg_id)

    Raises:
        ConfigError: If any required credentials are missing

    Example:
        >>> creds = get_scm_credentials()
        >>> print(creds["client_id"])
    """
    return {
        "client_id": get_config("SCM_CLIENT_ID", required=True),
        "client_secret": get_config("SCM_CLIENT_SECRET", required=True),
        "tsg_id": get_config("SCM_TSG_ID", required=True),
    }


def get_langsmith_config() -> dict[str, Optional[str]]:
    """
    Get LangSmith tracing configuration.

    Returns:
        Dictionary with LangSmith config (optional, returns None for unset values)

    Example:
        >>> config = get_langsmith_config()
        >>> if config["tracing_enabled"]:
        ...     print(f"Tracing to project: {config['project']}")
    """
    return {
        "tracing_enabled": get_config("LANGCHAIN_TRACING_V2", default="false").lower()
        == "true",
        "api_key": get_config("LANGSMITH_API_KEY"),
        "workspace_id": get_config("LANGSMITH_WORKSPACE_ID"),
        "project": get_config("LANGCHAIN_PROJECT", default="scm-nlp-workflow"),
        "endpoint": get_config(
            "LANGCHAIN_ENDPOINT", default="https://api.smith.langchain.com"
        ),
    }


def print_config_status() -> None:
    """
    Print configuration status for debugging.

    Displays which environment variables are set and which are missing.
    Useful for troubleshooting configuration issues.

    Example:
        >>> print_config_status()
        Configuration Status:
        ✅ SCM_CLIENT_ID: Set
        ✅ SCM_CLIENT_SECRET: Set
        ✅ SCM_TSG_ID: Set
        ❌ LANGSMITH_API_KEY: Not set
    """
    print("Configuration Status:")
    print("=" * 50)

    # Required
    print("\nRequired:")
    for var in [
        "SCM_CLIENT_ID",
        "SCM_CLIENT_SECRET",
        "SCM_TSG_ID",
        "ANTHROPIC_API_KEY",
    ]:
        status = "✅ Set" if os.getenv(var) else "❌ Not set"
        print(f"  {var}: {status}")

    # Optional (LangSmith)
    print("\nOptional (LangSmith):")
    for var in [
        "LANGCHAIN_TRACING_V2",
        "LANGSMITH_API_KEY",
        "LANGSMITH_WORKSPACE_ID",
        "LANGCHAIN_PROJECT",
    ]:
        status = "✅ Set" if os.getenv(var) else "❌ Not set"
        print(f"  {var}: {status}")

    print("=" * 50)
