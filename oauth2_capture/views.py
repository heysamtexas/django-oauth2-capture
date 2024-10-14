import logging
import secrets

from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import QuerySet
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import DeleteView, ListView

from oauth2_capture.models import OAuthToken
from oauth2_capture.services.oauth2 import OAuth2ProviderFactory

logger = logging.getLogger(__name__)


def oauth2_callback(request: HttpRequest, provider: str) -> HttpResponse:
    """Finalize the Oauth2 flow, which is called by the OAuth2 provider after the user has authorized the app.

    Args:
        request (HttpRequest): The request object.
        provider (str): The OAuth2 provider name.

    Returns:
        HttpResponse: The response object

    """
    try:
        oauth2_provider = OAuth2ProviderFactory.get_provider(provider)
    except ValueError as e:
        return HttpResponse(str(e), status=400)

    code = request.GET.get("code")
    redirect_uri = request.build_absolute_uri(f"/oauth2_capture/{provider}/callback/")

    token_data = oauth2_provider.exchange_code_for_token(code, redirect_uri, request)

    msg = f"Token data: {token_data}"
    logger.debug(msg)

    access_token = token_data.get("access_token")

    if access_token:
        user_info = oauth2_provider.get_user_info(access_token)

        oauth_token, created = OAuthToken.objects.get_or_create(
            provider=provider,
            user_id=user_info.get("id"),
            owner=request.user,
        )
        oauth2_provider.update_token(oauth_token, token_data, user_info)

        return HttpResponse(f"{provider.capitalize()} account connected successfully.")

    return HttpResponse(
        f"Failed to connect {provider.capitalize()} account.", status=400
    )


def initiate_oauth2(request: HttpRequest, provider: str) -> HttpResponse:
    """Initiate the OAuth2 flow, which redirects the user to the OAuth2 provider's authorization page.

    Args:
        request (HttpRequest): The request object.
        provider (str): The OAuth2 provider name.

    Returns:
        HttpResponse: The response object

    """
    try:
        oauth2_provider = OAuth2ProviderFactory.get_provider(provider)
    except ValueError as e:
        return HttpResponse(str(e), status=400)

    state = secrets.token_urlsafe(32)
    redirect_uri = request.build_absolute_uri(f"/oauth2_capture/{provider}/callback/")
    auth_url = oauth2_provider.get_authorization_url(state, redirect_uri, request)

    # Store state in session for later verification
    request.session[f"{provider}_oauth_state"] = state

    logger.debug("Redirecting to %s", auth_url)
    return redirect(auth_url)


class DeleteOAuthTokenView(LoginRequiredMixin, DeleteView):
    """View for deleting an OAuth token."""

    model = OAuthToken
    success_url = reverse_lazy("oauth2_capture:list")

    def get_queryset(self) -> QuerySet:
        """Return the queryset of OAuth tokens owned by the current user."""
        return super().get_queryset().filter(owner=self.request.user)


class OAuthListView(LoginRequiredMixin, ListView):
    """View to list all the OAuth2 connections."""

    model = OAuthToken
    context_object_name = "connections"

    def get_queryset(self) -> QuerySet:
        """Get the queryset of OAuth2 connections."""
        return self.request.user.oauth_tokens.all()
