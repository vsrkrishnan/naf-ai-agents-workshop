"""
SCM client initialization and management.

Provides factory function for creating Strata Cloud Manager (SCM) client instances
with credentials loaded from environment variables.
"""

import os

from scm.client import ScmClient


def get_scm_client() -> ScmClient:
    """
    Initialize and return an SCM client instance.

    Loads credentials from environment variables:
    - SCM_CLIENT_ID: Service account client ID
    - SCM_CLIENT_SECRET: Service account secret
    - SCM_TSG_ID: Tenant Service Group ID

    Returns:
        ScmClient: Authenticated SCM client ready for API calls

    Raises:
        KeyError: If required environment variables are not set

    Example:
        >>> client = get_scm_client()
        >>> tags = client.tag.list(folder="Texas")
    """
    return ScmClient(
        client_id=os.getenv("SCM_CLIENT_ID"),
        client_secret=os.getenv("SCM_CLIENT_SECRET"),
        tsg_id=os.getenv("SCM_TSG_ID"),
    )
