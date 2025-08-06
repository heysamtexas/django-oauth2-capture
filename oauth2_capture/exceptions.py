"""Simple token-related exceptions for oauth2_capture."""


class TokenRefreshError(Exception):
    """Token refresh failed. Re-authorization may be required."""

    def __init__(self, message: str, provider: str | None = None) -> None:
        """Initialize TokenRefreshError with message and optional provider."""
        super().__init__(message)
        self.provider = provider
