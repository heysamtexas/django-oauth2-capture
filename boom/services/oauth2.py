from __future__ import annotations

import base64
import logging
from abc import ABC, abstractmethod
from datetime import timedelta
from typing import TYPE_CHECKING
from urllib.parse import urlencode

import requests
from django.conf import settings
from django.utils import timezone

from boom.models import OAuthToken

if TYPE_CHECKING:
    from django.contrib.auth.models import User

logger = logging.getLogger(__name__)


class OAuth2Provider(ABC):
    """Base class for OAuth2 providers."""

    def __init__(self, provider_name: str) -> None:
        """Initialize the OAuth2 provider.

        Args:
            provider_name (str): The name of the provider.

        """
        self.provider_name = provider_name
        self.config = settings.OAUTH2_CONFIG[provider_name]

    @property
    @abstractmethod
    def authorize_url(self) -> str:
        """The URL to authorize the user."""

    @property
    @abstractmethod
    def token_url(self) -> str:
        """The URL to exchange the code for a token."""

    @property
    @abstractmethod
    def user_info_url(self) -> str:
        """The URL to get the user info."""

    @abstractmethod
    def get_user_info(self, access_token: str) -> dict:
        """Get the user info from the provider.

        Args:
            access_token (str): The access token.

        Returns:
            dict: The user info.

        """

    def get_authorization_url(self, state: str, redirect_uri: str) -> str:
        """Get the authorization URL for the provider.

        Args:
            state (str): The state parameter.
            redirect_uri (str): The redirect URI.

        Returns:
            str: The authorization URL.

        """
        params = {
            "client_id": self.config["client_id"],
            "redirect_uri": redirect_uri,
            "response_type": "code",
            "state": state,
            "scope": self.config["scope"],
        }
        return f"{self.authorize_url}?{urlencode(params)}"

    @abstractmethod
    def exchange_code_for_token(self, code: str, redirect_uri: str) -> dict:
        """Exchange the auth code for an access token.

        Args:
            code (str): The code.
            redirect_uri (str): The redirect URI.

        Returns:
            dict: The token data.

        """

    def refresh_token(self, refresh_token: str) -> dict:
        """Refresh the access token.

        Args:
            refresh_token (str): The refresh token.

        Returns:
            dict: The token data.

        """
        data = {
            "grant_type": "refresh_token",
            "refresh_token": refresh_token,
            "client_id": self.config["client_id"],
            "client_secret": self.config["client_secret"],
        }
        headers = {"Content-Type": "application/x-www-form-urlencoded"}
        response = requests.post(self.token_url, data=data, headers=headers, timeout=10)
        return response.json()

    def get_valid_token(self, user: User) -> str | None:
        """Get a valid access token for the user. If the token is expired, it will be refreshed.

        Args:
            user (User): The user.

        Returns:
            str|None: The access token or None if there is no token.

        """
        try:
            oauth_token = OAuthToken.objects.get(
                provider=self.provider_name, owner=user
            )
        except OAuthToken.DoesNotExist:
            return None

        if oauth_token.expires_at <= timezone.now():
            token_data = self.refresh_token(oauth_token.refresh_token)
            self.update_token(oauth_token, token_data)

        return oauth_token.access_token

    def update_token(
        self, oauth_token: OAuthToken, token_data: dict, user_info: dict
    ) -> None:
        """Update the OAuth token with the new data.

        Args:
            oauth_token (OAuthToken): The OAuth token to update.
            token_data (dict): The new token data.
            user_info (dict): The user info.

        Returns:
            None

        """
        oauth_token.access_token = token_data["access_token"]
        oauth_token.refresh_token = token_data.get(
            "refresh_token", oauth_token.refresh_token
        )
        oauth_token.expires_at = timezone.now() + timedelta(
            seconds=token_data["expires_in"]
        )
        if "refresh_token_expires_in" in token_data:
            oauth_token.refresh_token_expires_at = timezone.now() + timedelta(
                seconds=token_data["refresh_token_expires_in"]
            )
        oauth_token.scope = token_data.get("scope")
        oauth_token.token_type = token_data.get("token_type")

        # Update the user info
        oauth_token.profile_json = user_info
        oauth_token.name = user_info.get("name")

        oauth_token.save()


class TwitterOAuth2Provider(OAuth2Provider):
    """Twitter OAuth2 provider."""

    @property
    def authorize_url(self) -> str:
        """The URL to authorize the user."""
        return "https://twitter.com/i/oauth2/authorize"

    @property
    def token_url(self) -> str:
        """The URL to exchange the code for a token."""
        return "https://api.twitter.com/2/oauth2/token"

    @property
    def user_info_url(self) -> str:
        """The URL to get the user info."""
        return "https://api.twitter.com/2/users/me"

    def get_authorization_url(self, state: str, redirect_uri: str) -> str:
        """Get the authorization URL for Twitter. Override to include PKCE.

        Args:
            state (str): The state parameter.
            redirect_uri (str): The redirect URI.

        Returns:
            str: The authorization URL.

        """
        params = {
            "client_id": self.config["client_id"],
            "redirect_uri": redirect_uri,
            "response_type": "code",
            "state": state,
            "scope": self.config["scope"],
            "code_challenge": "challenge",
            "code_challenge_method": "plain",
        }
        return f"{self.authorize_url}?{urlencode(params)}"

    def get_user_info(self, access_token: str) -> dict:
        """Get the user info from Twitter.

        Args:
            access_token (str): The access token.

        Returns:
            dict: The user info.

        """
        headers = {"Authorization": f"Bearer {access_token}"}
        params = {"user.fields": "id,name,username,profile_image_url,description"}
        response = requests.get(
            self.user_info_url, headers=headers, params=params, timeout=10
        )
        return response.json().get("data", {})

    def exchange_code_for_token(self, code: str, redirect_uri: str) -> dict:
        """Exchange the auth code for an access token.

        Args:
            code (str): The code.
            redirect_uri (str): The redirect URI.

        Returns:
            dict: The token data.

        """
        # Override to include PKCE
        data = {
            "grant_type": "authorization_code",
            "code": code,
            "redirect_uri": redirect_uri,
            "client_id": self.config["client_id"],
            "client_secret": self.config["client_secret"],
            "code_verifier": "challenge",
        }

        # Use Basic Auth for Twitter
        credentials = f"{self.config['client_id']}:{self.config['client_secret']}"
        encoded_credentials = base64.b64encode(credentials.encode()).decode()
        headers = {
            "Content-Type": "application/x-www-form-urlencoded",
            "Authorization": f"Basic {encoded_credentials}",
        }

        response = requests.post(self.token_url, data=data, headers=headers, timeout=10)

        logger.debug("Twitter token response: %s", response.json())
        return response.json()


class LinkedInOAuth2Provider(OAuth2Provider):
    """LinkedIn OAuth2 provider."""

    @property
    def authorize_url(self) -> str:
        """The URL to authorize the user."""
        return "https://www.linkedin.com/oauth/v2/authorization"

    @property
    def token_url(self) -> str:
        """The URL to exchange the code for a token."""
        return "https://www.linkedin.com/oauth/v2/accessToken"

    @property
    def user_info_url(self) -> str:
        """The URL to get the user info."""
        return "https://api.linkedin.com/v2/userinfo"

    def get_user_info(self, access_token: str) -> dict:
        """Get the user info from LinkedIn.

        Args:
            access_token (str): The access token.

        Returns:
            dict: The user info.

        """
        headers = {"Authorization": f"Bearer {access_token}"}
        response = requests.get(self.user_info_url, headers=headers, timeout=10)
        res = response.json()

        # map the sub claim to id
        res["id"] = res.get("sub")

        logger.debug("LinkedIn user info: %s", res)
        return res

    def exchange_code_for_token(self, code: str, redirect_uri: str) -> dict:
        """Exchange the auth code for an access token.

        Args:
            code (str): The code.
            redirect_uri (str): The redirect URI.

        Returns:
            dict: The token data.

        """
        data = {
            "grant_type": "authorization_code",
            "code": code,
            "redirect_uri": redirect_uri,
            "client_id": self.config["client_id"],
            "client_secret": self.config["client_secret"],
        }
        headers = {"Content-Type": "application/x-www-form-urlencoded"}
        response = requests.post(self.token_url, data=data, headers=headers, timeout=10)
        return response.json()


class GitHubOAuth2Provider(OAuth2Provider):
    """GitHub OAuth2 provider."""

    @property
    def authorize_url(self) -> str:
        """The URL to authorize the user."""
        return "https://github.com/login/oauth/authorize"

    @property
    def token_url(self) -> str:
        """The URL to exchange the code for a token."""
        return "https://github.com/login/oauth/access_token"

    @property
    def user_info_url(self) -> str:
        """The URL to get the user info."""
        return "https://api.github.com/user"

    def get_user_info(self, access_token: str) -> dict:
        """Get the user info from GitHub.

        Args:
            access_token (str): The access token.

        Returns:
            dict: The user info.

        """
        headers = {"Authorization": f"token {access_token}"}
        response = requests.get(self.user_info_url, headers=headers, timeout=10)

        msg = f"\n\n{self.provider_name} user info response: {response.text}\n\n"
        logger.debug(msg)

        res = response.json()

        res["name"] = res["login"] if res["name"] is None else res["name"]

        return res

    def exchange_code_for_token(self, code: str, redirect_uri: str) -> dict:
        """Exchange the auth code for an access token.

        Args:
            code (str): The code.
            redirect_uri (str): The redirect URI.

        Returns:
            dict: The token data.

        """
        data = {
            "client_id": self.config["client_id"],
            "client_secret": self.config["client_secret"],
            "code": code,
            "redirect_uri": redirect_uri,
        }
        headers = {"Accept": "application/json"}
        response = requests.post(self.token_url, data=data, headers=headers, timeout=10)

        return response.json()


class OAuth2ProviderFactory:
    """Factory class to get the OAuth2 provider."""

    @staticmethod
    def get_provider(provider_name: str) -> OAuth2Provider:
        """Get the OAuth2 provider.

        Args:
            provider_name (str): The name of the provider.

        Returns:
            OAuth2Provider: The OAuth2 provider.

        """
        providers = {
            "twitter": TwitterOAuth2Provider,
            "linkedin": LinkedInOAuth2Provider,
            "github": GitHubOAuth2Provider,
        }
        provider_class = providers.get(provider_name)
        if not provider_class:
            msg = f"Unsupported provider: {provider_name}"
            raise ValueError(msg)
        return provider_class(provider_name)
