"""Test cases for the demo app."""

from unittest.mock import Mock, patch

from django.contrib.auth.models import User
from django.contrib.messages import get_messages
from django.test import Client, TestCase
from django.urls import reverse

from oauth2_capture.exceptions import TokenRefreshError
from oauth2_capture.models import OAuthToken


class TokenRefreshErrorHandlingTest(TestCase):
    """Test the demo app's handling of TokenRefreshError exceptions."""

    def setUp(self):
        """Set up test data."""
        self.client = Client()
        self.user = User.objects.create_user(username="testuser", password="testpass123")
        self.client.login(username="testuser", password="testpass123")

        # Create a test token
        self.token = OAuthToken.objects.create(
            provider="twitter",
            access_token="test_access_token",
            refresh_token="test_refresh_token",
            owner=self.user,
            user_id="twitter_user_123",
            token_type="Bearer",
        )

        self.social_post_url = reverse("demo:social_post", kwargs={"provider": "twitter", "slug": self.token.slug})

    @patch("demo.views.OAuth2ProviderFactory.get_provider")
    def test_social_post_token_refresh_error_shows_reauth_template(self, mock_get_provider):
        """Test that TokenRefreshError results in friendly reauth template."""
        # Mock the provider to raise TokenRefreshError
        mock_provider_instance = Mock()
        mock_provider_instance.get_valid_token.side_effect = TokenRefreshError(
            "Token refresh failed for twitter. Re-authorization may be required.", provider="twitter"
        )
        mock_get_provider.return_value = mock_provider_instance

        # Make the POST request
        response = self.client.post(self.social_post_url)

        # Verify the response
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "reauth_needed.html")

        # Check context variables
        self.assertEqual(response.context["provider"], "twitter")
        self.assertEqual(response.context["provider_title"], "Twitter")
        self.assertEqual(response.context["token"], self.token)
        self.assertIn("Token refresh failed for twitter", response.context["error_message"])

        # Verify user sees a warning message
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), "Your Twitter connection has expired. Please reconnect to continue posting.")

    @patch("demo.views.OAuth2ProviderFactory.get_provider")
    def test_reauth_template_content(self, mock_get_provider):
        """Test that the reauth template contains expected content."""
        # Mock TokenRefreshError
        mock_provider_instance = Mock()
        mock_provider_instance.get_valid_token.side_effect = TokenRefreshError("Test error message", provider="twitter")
        mock_get_provider.return_value = mock_provider_instance

        response = self.client.post(self.social_post_url)
        # Check template content
        self.assertContains(response, "Reconnection Required")
        self.assertContains(response, "Your <strong>Twitter</strong> connection has expired")
        self.assertContains(response, "🔗 Reconnect Twitter")
        self.assertContains(response, "Test error message")
        self.assertContains(response, "/oauth2/twitter/connect/")
        self.assertContains(response, "← Back to Home")

    @patch("demo.views.twitter_post")
    @patch("demo.views.OAuth2ProviderFactory.get_provider")
    def test_social_post_success_flow_unchanged(self, mock_get_provider, mock_twitter_post):
        """Test that successful token validation continues normal flow."""
        # Mock successful token validation
        mock_provider_instance = Mock()
        mock_provider_instance.get_valid_token.return_value = "valid_access_token"
        mock_get_provider.return_value = mock_provider_instance

        # Mock successful twitter post
        mock_twitter_post.return_value = (
            "https://twitter.com/test/status/123",
            "Tweet created: https://twitter.com/test/status/123",
        )

        response = self.client.post(self.social_post_url)

        # Verify successful flow
        self.assertEqual(response.status_code, 302)  # Redirect to home
        self.assertEqual(response.url, "/")

        # Verify success message
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertIn("Tweet created:", str(messages[0]))

        # Verify functions were called correctly
        mock_provider_instance.get_valid_token.assert_called_once_with(self.token)
        mock_twitter_post.assert_called_once_with(self.token, "valid_access_token")

    @patch("demo.views.OAuth2ProviderFactory.get_provider")
    def test_social_post_unsupported_provider(self, mock_get_provider):
        """Test handling of unsupported provider."""
        # Create token for unsupported provider
        unsupported_token = OAuthToken.objects.create(
            provider="unsupported",
            access_token="test_token",
            owner=self.user,
            user_id="unsupported_123",
            token_type="Bearer",
        )

        # Mock successful token validation
        mock_provider_instance = Mock()
        mock_provider_instance.get_valid_token.return_value = "valid_token"
        mock_get_provider.return_value = mock_provider_instance

        url = reverse("demo:social_post", kwargs={"provider": "unsupported", "slug": unsupported_token.slug})

        response = self.client.post(url)

        # Should redirect to home with error message
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, "/")

        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), "Unsupported provider: unsupported")

    @patch("demo.views.OAuth2ProviderFactory.get_provider")
    def test_social_post_requires_authentication(self, mock_get_provider):
        """Test that social_post view requires user authentication."""
        # Logout the user
        self.client.logout()

        response = self.client.post(self.social_post_url)

        # Should redirect to login
        self.assertEqual(response.status_code, 302)
        self.assertIn("login", response.url)

    @patch("demo.views.OAuth2ProviderFactory.get_provider")
    def test_social_post_token_not_found(self, mock_get_provider):
        """Test behavior when token doesn't exist."""
        # Use non-existent slug
        fake_url = reverse("demo:social_post", kwargs={"provider": "twitter", "slug": "nonexistent-slug"})

        response = self.client.post(fake_url)

        # Should return 404
        self.assertEqual(response.status_code, 404)

    @patch("demo.views.OAuth2ProviderFactory.get_provider")
    def test_different_providers_token_refresh_error(self, mock_get_provider):
        """Test TokenRefreshError handling works for different providers."""
        providers = ["linkedin", "github", "reddit"]
        for provider in providers:
            with self.subTest(provider=provider):
                # Create token for this provider
                token = OAuthToken.objects.create(
                    provider=provider,
                    access_token="test_token",
                    owner=self.user,
                    user_id=f"{provider}_user_123",
                    token_type="Bearer",
                )

                # Mock TokenRefreshError
                mock_provider_instance = Mock()
                mock_provider_instance.get_valid_token.side_effect = TokenRefreshError(
                    f"Token refresh failed for {provider}", provider=provider
                )
                mock_get_provider.return_value = mock_provider_instance

                url = reverse("demo:social_post", kwargs={"provider": provider, "slug": token.slug})

                response = self.client.post(url)

                # Verify template is rendered with correct provider info
                self.assertEqual(response.status_code, 200)
                self.assertTemplateUsed(response, "reauth_needed.html")
                self.assertEqual(response.context["provider"], provider)
                self.assertEqual(response.context["provider_title"], provider.title())
                self.assertContains(response, f"/oauth2/{provider}/connect/")
