from __future__ import annotations

import base64
import contextlib
import hashlib
import logging
import secrets
import time
from abc import ABC, abstractmethod
from datetime import timedelta
from typing import TYPE_CHECKING
from urllib.parse import urlencode

import requests
from django.conf import settings
from django.utils import timezone
from requests.auth import HTTPBasicAuth

if TYPE_CHECKING:
    from collections.abc import Callable

    from django.http import HttpRequest

    from oauth2_capture.models import OAuthToken


logger = logging.getLogger(__name__)


def generate_code_verifier(length: int = 128) -> str:
    """Generate a code verifier for PKCE.

    Args:
        length (int): The length of the code verifier.

    Returns:
        str: The code verifier.

    """
    return secrets.token_urlsafe(length)


def generate_code_challenge(verifier: str) -> str:
    """Generate a code challenge for PKCE.

    Args:
        verifier (str): The code verifier.

    Returns:
        str: The code challenge.

    """
    sha256 = hashlib.sha256(verifier.encode("utf-8")).digest()
    return base64.urlsafe_b64encode(sha256).decode("utf-8").rstrip("=")


def retry_with_backoff(
    request_func: Callable[[], requests.Response], max_retries: int = 5, fallback_delays: tuple = (5, 10, 20, 40, 60)
) -> requests.Response:
    """Retry a request with exponential backoff.

    Args:
        request_func (Callable): The function to call for the request.
        max_retries (int): The maximum number of retries.
        fallback_delays (tuple): The fallback delays in seconds.

    Returns:
        requests.Response: The response from the request.

    """
    for attempt in range(max_retries):
        response = request_func()
        if response.status_code != 429:  # noqa: PLR2004
            return response
        retry_after = response.headers.get("Retry-After")

        delay = fallback_delays[min(attempt, len(fallback_delays) - 1)]

        if retry_after:
            with contextlib.suppress(ValueError):
                delay = int(retry_after)

        time.sleep(delay)
    return response  # Return last response after max retries


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

    def get_authorization_url(
        self,
        state: str,
        redirect_uri: str,
        request: HttpRequest,  # noqa: ARG002
    ) -> str:
        """Get the authorization URL for the provider.

        Args:
            state (str): The state parameter.
            redirect_uri (str): The redirect URI.
            request (HttpRequest): The request object.

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
    def exchange_code_for_token(self, code: str, redirect_uri: str, request: HttpRequest) -> dict:
        """Exchange the auth code for an access token.

        Args:
            code (str): The code.
            redirect_uri (str): The redirect URI.
            request (HttpRequest): The request object.

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

        # Encode the client_id and client_secret
        credentials = f"{self.config['client_id']}:{self.config['client_secret']}"
        encoded_credentials = base64.b64encode(credentials.encode()).decode()

        headers = {
            "Authorization": f"Basic {encoded_credentials}",
            "Content-Type": "application/x-www-form-urlencoded",
        }

        def do_request() -> requests.Response:
            return requests.post(self.token_url, data=data, headers=headers, timeout=10)

        response = retry_with_backoff(do_request)
        if response.status_code != 200:  # noqa: PLR2004
            logger.error("Token refresh failed: %s - %s", response.status_code, response.text)
            return {}
        return response.json()

    def get_valid_token(self, oauth_token: OAuthToken) -> str | None:
        """Get a valid access token for the user. If the token is expired, it will be refreshed.

        Args:
            oauth_token (OAuthToken): The user.

        Returns:
            str|None: The access token or None if there is no token.

        """
        if oauth_token.expires_at and oauth_token.expires_at <= timezone.now():
            msg = f"Token for {oauth_token.provider}:{oauth_token.name} has expired. Refreshing..."
            logger.debug(msg)
            token_data = self.refresh_token(oauth_token.refresh_token)

            # Check if the refresh was successful
            if not token_data or "access_token" not in token_data:
                logger.error(
                    "Failed to refresh token for %s:%s. Response: %s",
                    oauth_token.provider,
                    oauth_token.name,
                    token_data,
                )
                return None

            try:
                self.update_token(
                    oauth_token=oauth_token,
                    token_data=token_data,
                    user_info=self.get_user_info(token_data["access_token"]),
                )
            except Exception:
                logger.exception("Error updating token for %s:%s.", oauth_token.provider, oauth_token.name)
                return None

        logger.debug("Token for %s:%s is valid", oauth_token.provider, oauth_token.name)
        return oauth_token.access_token

    def update_token(self, oauth_token: OAuthToken, token_data: dict, user_info: dict) -> None:
        """Update the OAuth token with the new data.

        Args:
            oauth_token (OAuthToken): The OAuth token to update.
            token_data (dict): The new token data.
            user_info (dict): The user info.

        Returns:
            None

        """
        logger.debug(token_data)

        oauth_token.access_token = token_data["access_token"]
        oauth_token.refresh_token = token_data.get("refresh_token", oauth_token.refresh_token)

        if "expires_in" in token_data:
            oauth_token.expires_at = timezone.now() + timedelta(seconds=token_data["expires_in"])
        if "refresh_token_expires_in" in token_data:
            oauth_token.refresh_token_expires_at = timezone.now() + timedelta(
                seconds=token_data["refresh_token_expires_in"]
            )
        oauth_token.scope = token_data.get("scope", self.config["scope"])
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

    def get_authorization_url(self, state: str, redirect_uri: str, request: HttpRequest) -> str:
        """Get the authorization URL for Twitter. Override to include PKCE.

        Args:
            state (str): The state parameter.
            redirect_uri (str): The redirect URI.
            request (HttpRequest): The request object.

        Returns:
            str: The authorization URL.

        """
        # Generate code verifier and code challenge
        code_verifier = generate_code_verifier()
        code_challenge = generate_code_challenge(code_verifier)

        request.session["code_verifier"] = code_verifier

        params = {
            "client_id": self.config["client_id"],
            "redirect_uri": redirect_uri,
            "response_type": "code",
            "state": state,
            "scope": self.config["scope"],
            "code_challenge": code_challenge,
            "code_challenge_method": "S256",
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
        response = requests.get(self.user_info_url, headers=headers, params=params, timeout=10)
        return response.json().get("data", {})

    def exchange_code_for_token(self, code: str, redirect_uri: str, request: HttpRequest) -> dict:
        """Exchange the auth code for an access token.

        Args:
            code (str): The code.
            redirect_uri (str): The redirect URI.
            request (HttpRequest): The request object.

        Returns:
            dict: The token data.

        """
        code_verifier = request.session.get("code_verifier")

        # Override to include PKCE
        data = {
            "grant_type": "authorization_code",
            "code": code,
            "redirect_uri": redirect_uri,
            "client_id": self.config["client_id"],
            "client_secret": self.config["client_secret"],
            "code_verifier": code_verifier,
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

    def exchange_code_for_token(
        self,
        code: str,
        redirect_uri: str,
        request: HttpRequest,  # noqa: ARG002
    ) -> dict:
        """Exchange the auth code for an access token.

        Args:
            code (str): The code.
            redirect_uri (str): The redirect URI.
            request (HttpRequest): The request object.

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

    def exchange_code_for_token(
        self,
        code: str,
        redirect_uri: str,
        request: HttpRequest,  # noqa: ARG002
    ) -> dict:
        """Exchange the auth code for an access token.

        Args:
            code (str): The code.
            redirect_uri (str): The redirect URI.
            request (HttpRequest): The request object.

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


class RedditOAuth2Provider(OAuth2Provider):
    """Reddit OAuth2 provider."""

    @property
    def authorize_url(self) -> str:
        """The URL to authorize the user."""
        return "https://www.reddit.com/api/v1/authorize"

    @property
    def token_url(self) -> str:
        """The URL to exchange the code for a token."""
        return "https://www.reddit.com/api/v1/access_token"

    @property
    def user_info_url(self) -> str:
        """The URL to get the user info."""
        return "https://oauth.reddit.com/api/v1/me"

    def get_user_info(self, access_token: str) -> dict:
        """Get the user info from Reddit.

        Args:
            access_token (str): The access token.

        Returns:
            dict: The user info.

        """
        headers = {"Authorization": f"Bearer {access_token}"}
        response = requests.get(self.user_info_url, headers=headers, timeout=10)
        return response.json()

    def exchange_code_for_token(
        self,
        code: str,
        redirect_uri: str,
        request: HttpRequest,  # noqa: ARG002
    ) -> dict:
        """Exchange the auth code for an access token.

        Args:
            code (str): The code.
            redirect_uri (str): The redirect URI.
            request (HttpRequest): The request object.

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
        headers = {
            "User-Agent": "Oauth2Capture/1.0 by simplecto",
        }

        auth = HTTPBasicAuth(self.config["client_id"], self.config["client_secret"])
        response = requests.post(self.token_url, data=data, auth=auth, headers=headers, timeout=10)

        return response.json()

    def refresh_token(self, refresh_token: str) -> dict:
        """Refresh the Reddit access token.

        Reddit requires HTTP Basic Auth with the client_id and client_secret
        *only* in the Authorization header plus a custom User-Agent on *every*
        request. Supplying client credentials in the POST body can trigger a
        403, so we keep the body minimal.

        Args:
            refresh_token (str): The stored refresh token.

        Returns:
            dict: The token response data, or an empty dict on failure.

        """
        data = {
            "grant_type": "refresh_token",
            "refresh_token": refresh_token,
        }

        # Reddit mandates Basic Auth for confidential apps
        auth = HTTPBasicAuth(self.config["client_id"], self.config["client_secret"])
        headers = {
            "User-Agent": "Oauth2Capture/1.0 by simplecto",
        }

        response = requests.post(self.token_url, data=data, auth=auth, headers=headers, timeout=10)

        # Log useful info for debugging
        if response.status_code != 200:  # noqa: PLR2004
            logger.error("Reddit refresh failed: %s - %s", response.status_code, response.text)
            return {}

        return response.json()

    def get_authorization_url(
        self,
        state: str,
        redirect_uri: str,
        request: HttpRequest,  # noqa: ARG002
    ) -> str:
        """Get the authorization URL for Reddit.

        Args:
            state (str): The state parameter.
            redirect_uri (str): The redirect URI.
            request (HttpRequest): The request object.

        Returns:
            str: The authorization URL.

        """
        params = {
            "client_id": self.config["client_id"],
            "redirect_uri": redirect_uri,
            "response_type": "code",
            "state": state,
            "scope": self.config["scope"],
            "duration": "permanent",
        }
        return f"{self.authorize_url}?{urlencode(params)}"


class PinterestOAuth2Provider(OAuth2Provider):
    """Pinterest OAuth2 provider."""

    @property
    def authorize_url(self) -> str:
        """The URL to authorize the user."""
        return "https://www.pinterest.com/oauth/"

    @property
    def token_url(self) -> str:
        """The URL to exchange the code for a token."""
        return "https://api.pinterest.com/v5/oauth/token"

    @property
    def user_info_url(self) -> str:
        """The URL to get the user info."""
        return "https://api.pinterest.com/v5/user_account"

    def get_user_info(self, access_token: str) -> dict:
        """Get the user info from Pinterest.

        Args:
            access_token (str): The access token.

        Returns:
            dict: The user info.

        """
        headers = {"Authorization": f"Bearer {access_token}"}
        response = requests.get(self.user_info_url, headers=headers, timeout=10)
        user_data = response.json()

        # Ensure we have the expected structure including id and name fields
        if "id" not in user_data and "username" in user_data:
            user_data["id"] = user_data["username"]

        # Set name if not present
        if "name" not in user_data or not user_data["name"]:
            user_data["name"] = user_data.get("username", "Pinterest User")

        logger.debug("Pinterest user info: %s", user_data)
        return user_data

    def exchange_code_for_token(
        self,
        code: str,
        redirect_uri: str,
        request: HttpRequest,  # noqa: ARG002
    ) -> dict:
        """Exchange the auth code for an access token.

        Args:
            code (str): The code.
            redirect_uri (str): The redirect URI.
            request (HttpRequest): The request object.

        Returns:
            dict: The token data.

        """
        data = {
            "grant_type": "authorization_code",
            "code": code,
            "redirect_uri": redirect_uri,
        }

        # Pinterest uses HTTP Basic auth for client authentication
        auth = HTTPBasicAuth(self.config["client_id"], self.config["client_secret"])
        headers = {"Content-Type": "application/x-www-form-urlencoded"}

        response = requests.post(self.token_url, data=data, auth=auth, headers=headers, timeout=10)

        return response.json()


class FacebookOAuth2Provider(OAuth2Provider):
    """Facebook OAuth2 provider."""

    @property
    def authorize_url(self) -> str:
        """The URL to authorize the user."""
        return "https://www.facebook.com/v19.0/dialog/oauth"

    @property
    def token_url(self) -> str:
        """The URL to exchange the code for a token."""
        return "https://graph.facebook.com/v19.0/oauth/access_token"

    @property
    def user_info_url(self) -> str:
        """The URL to get the user info."""
        return "https://graph.facebook.com/v19.0/me"

    def get_user_info(self, access_token: str) -> dict:
        """Get the user info from Facebook.

        Args:
            access_token (str): The access token.

        Returns:
            dict: The user info.

        """
        params = {
            "fields": "id,name,email,picture",
            "access_token": access_token,
        }
        response = requests.get(self.user_info_url, params=params, timeout=10)
        user_data = response.json()

        # Ensure proper structure
        if "picture" in user_data and "data" in user_data["picture"]:
            user_data["profile_image_url"] = user_data["picture"]["data"]["url"]

        logger.debug("Facebook user info: %s", user_data)
        return user_data

    def exchange_code_for_token(
        self,
        code: str,
        redirect_uri: str,
        request: HttpRequest,  # noqa: ARG002
    ) -> dict:
        """Exchange the auth code for an access token.

        Args:
            code (str): The code.
            redirect_uri (str): The redirect URI.
            request (HttpRequest): The request object.

        Returns:
            dict: The token data.

        """
        params = {
            "client_id": self.config["client_id"],
            "client_secret": self.config["client_secret"],
            "code": code,
            "redirect_uri": redirect_uri,
        }

        response = requests.get(self.token_url, params=params, timeout=10)
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
            "reddit": RedditOAuth2Provider,
            "pinterest": PinterestOAuth2Provider,
            "facebook": FacebookOAuth2Provider,
        }
        provider_class = providers.get(provider_name)
        if not provider_class:
            msg = f"Unsupported provider: {provider_name}"
            raise ValueError(msg)
        return provider_class(provider_name)
