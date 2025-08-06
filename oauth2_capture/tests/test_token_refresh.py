from django.test import TestCase, override_settings
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta
from unittest.mock import Mock, patch

from oauth2_capture.models import OAuthToken
from oauth2_capture.services.oauth2 import TwitterOAuth2Provider
from oauth2_capture.exceptions import TokenRefreshError


@override_settings(OAUTH2_CONFIG={
    'twitter': {
        'client_id': 'test_client_id',
        'client_secret': 'test_client_secret',
        'scope': 'tweet.read users.read tweet.write offline.access',
        'code_verifier': 'challenge'
    }
})
class TokenRefreshErrorHandlingTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.provider = TwitterOAuth2Provider('twitter')

        # Create an expired token
        self.expired_token = OAuthToken.objects.create(
            provider='twitter',
            access_token='expired_token',
            refresh_token='refresh_token_123',
            expires_at=timezone.now() - timedelta(hours=1),
            owner=self.user,
            user_id='twitter_user_123',
            token_type='Bearer'
        )

    @patch.object(TwitterOAuth2Provider, 'refresh_token')
    def test_refresh_failure_raises_exception(self, mock_refresh):
        """Test that refresh failure raises TokenRefreshError instead of returning None"""
        # Mock failed refresh (returns None or empty dict)
        mock_refresh.return_value = None

        with self.assertRaises(TokenRefreshError) as context:
            self.provider.get_valid_token(self.expired_token)

        # Check exception details
        self.assertEqual(context.exception.provider, 'twitter')
        self.assertIn('Token refresh failed for twitter', str(context.exception))
        self.assertIn('Re-authorization may be required', str(context.exception))

    @patch.object(TwitterOAuth2Provider, 'refresh_token')
    def test_refresh_invalid_response_raises_exception(self, mock_refresh):
        """Test that invalid refresh response raises TokenRefreshError"""
        # Mock invalid response (missing access_token)
        mock_refresh.return_value = {'error': 'invalid_grant'}

        with self.assertRaises(TokenRefreshError) as context:
            self.provider.get_valid_token(self.expired_token)

        self.assertEqual(context.exception.provider, 'twitter')

    @patch.object(TwitterOAuth2Provider, 'refresh_token')
    @patch.object(TwitterOAuth2Provider, 'get_user_info')
    def test_successful_refresh_works(self, mock_user_info, mock_refresh):
        """Test that successful refresh still works normally"""
        # Mock successful refresh
        mock_refresh.return_value = {
            'access_token': 'new_access_token',
            'expires_in': 3600,
            'refresh_token': 'new_refresh_token'
        }
        mock_user_info.return_value = {'id': '12345', 'name': 'Test User'}

        # Should not raise exception
        token = self.provider.get_valid_token(self.expired_token)

        # Should return the original token's access_token (which gets updated by update_token)
        self.assertIsNotNone(token)

    @patch.object(TwitterOAuth2Provider, 'update_token')
    @patch.object(TwitterOAuth2Provider, 'refresh_token')
    @patch.object(TwitterOAuth2Provider, 'get_user_info')
    def test_update_token_error_raises_exception(self, mock_user_info, mock_refresh, mock_update):
        """Test that update_token errors also raise TokenRefreshError"""
        # Mock successful refresh but failed update
        mock_refresh.return_value = {
            'access_token': 'new_access_token',
            'expires_in': 3600
        }
        mock_user_info.return_value = {'id': '12345'}
        mock_update.side_effect = Exception("Database error")

        with self.assertRaises(TokenRefreshError) as context:
            self.provider.get_valid_token(self.expired_token)

        self.assertEqual(context.exception.provider, 'twitter')
        self.assertIn('Error updating refreshed token', str(context.exception))

    def test_valid_token_returns_directly(self):
        """Test that non-expired tokens are returned directly"""
        # Create a valid (non-expired) token
        valid_token = OAuthToken.objects.create(
            provider='twitter',
            access_token='valid_token',
            expires_at=timezone.now() + timedelta(hours=1),
            owner=self.user,
            user_id='twitter_user_456',
            token_type='Bearer'
        )

        # Should return token without any refresh attempt
        token = self.provider.get_valid_token(valid_token)
        self.assertEqual(token, 'valid_token')
