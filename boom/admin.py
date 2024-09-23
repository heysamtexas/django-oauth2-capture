from django.contrib import admin

from boom.models import OAuthToken


@admin.register(OAuthToken)
class OAuthTokenAdmin(admin.ModelAdmin):
    """Admin view for OauthToken model."""

    list_display = ("owner", "provider", "name", "created_at")
    readonly_fields = ("owner", "name")
