from django.db import models
from shortuuid.django_fields import ShortUUIDField


class OAuthToken(models.Model):
    """Model to capture the OAuth token for API access."""

    provider = models.CharField(
        max_length=50,
        help_text="The name of the OAuth provider (e.g., 'google', 'github', 'facebook').",
    )
    slug = ShortUUIDField()
    access_token = models.TextField(help_text="The OAuth access token for API access.")
    expires_at = models.DateTimeField(
        null=True,
        blank=True,
        help_text="The exact expiration time of the access token.",
    )
    refresh_token = models.CharField(
        max_length=500,
        blank=True,
        default="",
        help_text="The refresh token, if provided by the OAuth provider.",
    )
    refresh_token_expires_at = models.DateTimeField(
        null=True, blank=True, help_text="The expiration time of the refresh token."
    )
    token_type = models.CharField(
        max_length=50,
        blank=True,
        default="",
        help_text="Type of the token, typically 'Bearer'.",
    )
    scope = models.TextField(
        blank=True,
        default="",
        help_text="Scopes granted by the OAuth provider (e.g., 'email profile').",
    )
    user_id = models.CharField(
        max_length=100,
        blank=True,
        default="",
        help_text="The unique ID of the user with the OAuth provider.",
    )
    owner = models.ForeignKey(
        "auth.User",
        on_delete=models.CASCADE,
        related_name="oauth_tokens",
        help_text="A reference to the local user this OAuth token is associated with.",
    )
    created_at = models.DateTimeField(
        auto_now_add=True, help_text="The timestamp when the token was issued."
    )

    profile_json = models.JSONField(null=True, blank=True)

    name = models.CharField(max_length=100, blank=True, default="")

    class Meta:
        """Metaclass options for the model."""

        unique_together = ("provider", "user_id")
        verbose_name = "OAuth Token"
        verbose_name_plural = "OAuth Tokens"

    def __str__(self) -> str:
        """Return the name of the OAuth token."""
        return f"{self.provider}: {self.name}"

    def is_expired(self) -> bool:
        """Check if the token has expired."""
        from django.utils import timezone

        if self.expires_at:
            return timezone.now() > self.expires_at
        return False

    @property
    def username(self) -> str:
        """Return the username associated with the OAuth token."""
        return (
            self.profile_json.get("username", "")
            or self.profile_json.get("login", "")
            or self.name
        )
