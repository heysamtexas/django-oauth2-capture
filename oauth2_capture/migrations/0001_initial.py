# Generated by Django 5.1.1 on 2024-09-23 11:23

import django.db.models.deletion
import shortuuid.django_fields
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="OAuthToken",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "provider",
                    models.CharField(
                        help_text="The name of the OAuth provider (e.g., 'google', 'github', 'facebook').",
                        max_length=50,
                    ),
                ),
                (
                    "slug",
                    shortuuid.django_fields.ShortUUIDField(
                        alphabet=None, length=22, max_length=22, prefix=""
                    ),
                ),
                (
                    "access_token",
                    models.CharField(
                        help_text="The OAuth access token for API access.",
                        max_length=500,
                    ),
                ),
                (
                    "expires_at",
                    models.DateTimeField(
                        blank=True,
                        help_text="The exact expiration time of the access token.",
                        null=True,
                    ),
                ),
                (
                    "refresh_token",
                    models.CharField(
                        blank=True,
                        default="",
                        help_text="The refresh token, if provided by the OAuth provider.",
                        max_length=500,
                    ),
                ),
                (
                    "refresh_token_expires_at",
                    models.DateTimeField(
                        blank=True,
                        help_text="The expiration time of the refresh token.",
                        null=True,
                    ),
                ),
                (
                    "token_type",
                    models.CharField(
                        blank=True,
                        default="",
                        help_text="Type of the token, typically 'Bearer'.",
                        max_length=50,
                    ),
                ),
                (
                    "scope",
                    models.TextField(
                        blank=True,
                        default="",
                        help_text="Scopes granted by the OAuth provider (e.g., 'email profile').",
                    ),
                ),
                (
                    "user_id",
                    models.CharField(
                        blank=True,
                        default="",
                        help_text="The unique ID of the user with the OAuth provider.",
                        max_length=100,
                    ),
                ),
                (
                    "created_at",
                    models.DateTimeField(
                        auto_now_add=True,
                        help_text="The timestamp when the token was issued.",
                    ),
                ),
                ("profile_json", models.JSONField(blank=True, null=True)),
                ("name", models.CharField(blank=True, default="", max_length=100)),
                (
                    "owner",
                    models.ForeignKey(
                        help_text="A reference to the local user this OAuth token is associated with.",
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="oauth_tokens",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "verbose_name": "OAuth Token",
                "verbose_name_plural": "OAuth Tokens",
                "unique_together": {("provider", "user_id")},
            },
        ),
    ]