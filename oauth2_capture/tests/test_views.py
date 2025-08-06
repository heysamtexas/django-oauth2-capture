from django.test import TestCase, RequestFactory
from django.contrib.auth.models import User
from django.contrib.sessions.middleware import SessionMiddleware
from django.http import HttpResponse
from unittest.mock import Mock, patch

from oauth2_capture.views import oauth2_callback, initiate_oauth2


class OAuthViewsTestCase(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.create_user(username='testuser', password='testpass')
        
    def _add_session_to_request(self, request):
        """Helper method to add session support to request"""
        middleware = SessionMiddleware(get_response=lambda req: HttpResponse())
        middleware.process_request(request)
        request.session.save()
        return request

    @patch('oauth2_capture.views.OAuth2ProviderFactory.get_provider')
    def test_oauth_callback_valid_state(self, mock_get_provider):
        """Test successful OAuth callback with valid state"""
        # Mock provider
        mock_provider = Mock()
        mock_provider.exchange_code_for_token.return_value = {'access_token': 'test_token'}
        mock_provider.get_user_info.return_value = {'id': '12345', 'name': 'Test User'}
        mock_provider.update_token = Mock()
        mock_get_provider.return_value = mock_provider
        
        # Create request with session
        request = self.factory.get('/oauth2/twitter/callback/', {
            'code': 'test_code',
            'state': 'test_state_value'
        })
        request.user = self.user
        request = self._add_session_to_request(request)
        
        # Set up session state (simulating what initiate_oauth2 would do)
        request.session['twitter_oauth_state'] = 'test_state_value'
        
        # Call the callback view
        response = oauth2_callback(request, 'twitter')
        
        # Verify successful response
        self.assertEqual(response.status_code, 200)
        self.assertIn('Twitter account connected successfully', response.content.decode())
        
        # Verify state was cleared from session
        self.assertNotIn('twitter_oauth_state', request.session)
        
        # Verify provider methods were called
        mock_provider.exchange_code_for_token.assert_called_once()
        mock_provider.get_user_info.assert_called_once_with('test_token')

    @patch('oauth2_capture.views.OAuth2ProviderFactory.get_provider')
    def test_oauth_callback_invalid_state(self, mock_get_provider):
        """Test OAuth callback with invalid state (CSRF protection)"""
        mock_provider = Mock()
        mock_get_provider.return_value = mock_provider
        
        # Create request with mismatched state
        request = self.factory.get('/oauth2/twitter/callback/', {
            'code': 'test_code',
            'state': 'malicious_state'
        })
        request.user = self.user
        request = self._add_session_to_request(request)
        
        # Set up different state in session
        request.session['twitter_oauth_state'] = 'legitimate_state'
        
        # Call the callback view
        response = oauth2_callback(request, 'twitter')
        
        # Verify rejection
        self.assertEqual(response.status_code, 400)
        self.assertIn('Invalid OAuth state', response.content.decode())
        self.assertIn('CSRF attack', response.content.decode())
        
        # Verify provider exchange was never called
        mock_provider.exchange_code_for_token.assert_not_called()

    @patch('oauth2_capture.views.OAuth2ProviderFactory.get_provider')
    def test_oauth_callback_missing_state(self, mock_get_provider):
        """Test OAuth callback with missing state parameter"""
        mock_provider = Mock()
        mock_get_provider.return_value = mock_provider
        
        # Create request without state parameter
        request = self.factory.get('/oauth2/twitter/callback/', {
            'code': 'test_code'
        })
        request.user = self.user
        request = self._add_session_to_request(request)
        
        # Set up state in session
        request.session['twitter_oauth_state'] = 'expected_state'
        
        # Call the callback view
        response = oauth2_callback(request, 'twitter')
        
        # Verify rejection
        self.assertEqual(response.status_code, 400)
        self.assertIn('Invalid OAuth state', response.content.decode())
        
        # Verify provider exchange was never called
        mock_provider.exchange_code_for_token.assert_not_called()

    @patch('oauth2_capture.views.OAuth2ProviderFactory.get_provider')
    def test_oauth_callback_user_denied_authorization(self, mock_get_provider):
        """Test OAuth callback when user denies authorization"""
        mock_provider = Mock()
        mock_get_provider.return_value = mock_provider
        
        # Create request with error parameter (user denied)
        request = self.factory.get('/oauth2/twitter/callback/', {
            'error': 'access_denied',
            'error_description': 'The user denied the request',
            'state': 'valid_state'
        })
        request.user = self.user
        request = self._add_session_to_request(request)
        
        # Set up valid state in session
        request.session['twitter_oauth_state'] = 'valid_state'
        
        # Call the callback view
        response = oauth2_callback(request, 'twitter')
        
        # Verify proper error handling
        self.assertEqual(response.status_code, 400)
        self.assertIn('Authorization denied', response.content.decode())
        
        # Verify state was still cleared (cleanup)
        self.assertNotIn('twitter_oauth_state', request.session)

    @patch('oauth2_capture.views.OAuth2ProviderFactory.get_provider')
    def test_oauth_callback_missing_code(self, mock_get_provider):
        """Test OAuth callback with missing authorization code"""
        mock_provider = Mock()
        mock_get_provider.return_value = mock_provider
        
        # Create request with valid state but no code
        request = self.factory.get('/oauth2/twitter/callback/', {
            'state': 'valid_state'
        })
        request.user = self.user
        request = self._add_session_to_request(request)
        
        # Set up valid state in session
        request.session['twitter_oauth_state'] = 'valid_state'
        
        # Call the callback view
        response = oauth2_callback(request, 'twitter')
        
        # Verify error handling
        self.assertEqual(response.status_code, 400)
        self.assertIn('No authorization code received', response.content.decode())
        
        # Verify state was cleared
        self.assertNotIn('twitter_oauth_state', request.session)