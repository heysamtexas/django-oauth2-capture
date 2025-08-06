# Error Scenario Testing Implementation

## Objective
Create comprehensive test coverage for all error scenarios that can occur during OAuth flows, token management, and API operations. This ensures the library handles failures gracefully and provides appropriate feedback to applications.

## Context
OAuth2 flows have many potential failure points that need robust testing:

**Network-Level Errors:**
- Provider API downtime
- Timeout issues
- DNS resolution failures
- SSL/TLS certificate problems

**OAuth Protocol Errors:**
- Invalid authorization codes
<<<<<<< HEAD
- Expired authorization codes  
=======
- Expired authorization codes
>>>>>>> faace65 (Add comprehensive OAuth security, testing, and coverage infrastructure)
- Invalid client credentials
- Scope permission denials
- User cancellation/denial

**Token Management Errors:**
- Expired access tokens
- Expired refresh tokens
- Revoked tokens
- Invalid token formats

**Application-Level Errors:**
- Missing configuration
- Invalid provider names
- Database connection issues
- Session handling problems

Currently, error handling is minimal and inconsistent across the codebase.

## Technical Details

### Error Scenario Categories

1. **Configuration Errors**
   - Missing OAUTH2_CONFIG settings
   - Invalid client_id/client_secret
   - Unsupported provider names

2. **OAuth Flow Errors**
   - Authorization code exchange failures
   - State parameter mismatches
   - User denial/cancellation
   - Provider-specific errors

3. **Network and API Errors**
   - Connection timeouts
   - HTTP error status codes (4xx, 5xx)
   - Malformed JSON responses
   - Rate limiting responses

4. **Token Lifecycle Errors**
   - Token expiration scenarios
   - Refresh token failures
   - Token revocation by user
   - Scope changes

5. **Database and Model Errors**
   - Unique constraint violations
   - Database connection failures
   - Model validation errors

### Testing Strategy
- Use `unittest.mock` to simulate various failure conditions
- Test both immediate failures and edge cases
- Verify error messages and logging
- Test error propagation through the stack
- Ensure graceful degradation

## Testing Requirements

1. **Configuration Error Tests**:
   - Missing provider configuration
   - Invalid configuration values
   - Provider not in factory

2. **OAuth Flow Error Tests**:
   - Invalid authorization codes
   - Expired codes
   - User cancellation flows
   - State parameter attacks

3. **API Error Tests**:
   - Network timeouts
   - HTTP error responses
   - Malformed JSON
   - Rate limiting

4. **Token Error Tests**:
   - Expired tokens with failed refresh
   - Revoked tokens
   - Invalid token formats
   - Missing refresh tokens

5. **Concurrent Access Tests**:
   - Multiple users accessing same provider
   - Race conditions in token updates
   - Session conflicts

## Dependencies
- Core OAuth flow tests (task 01) for baseline functionality
- Provider-specific tests (task 02) for provider error formats
- Better error responses (security task 04) for improved error handling

## Estimated Complexity
Medium (1-2 days)

## Files to Create
- `oauth2_capture/tests/test_error_scenarios.py`: Main error scenario tests
- `oauth2_capture/tests/test_network_errors.py`: Network and API error tests
- `oauth2_capture/tests/test_configuration_errors.py`: Configuration error tests
- `oauth2_capture/tests/utils/error_simulation.py`: Error simulation utilities

## Example Code

### Error Simulation Utilities
```python
# oauth2_capture/tests/utils/error_simulation.py
import requests
from unittest.mock import Mock
import json

class NetworkErrorSimulator:
    """Utilities to simulate various network error conditions."""
<<<<<<< HEAD
    
=======

>>>>>>> faace65 (Add comprehensive OAuth security, testing, and coverage infrastructure)
    @staticmethod
    def timeout_error():
        """Simulate a network timeout."""
        def side_effect(*args, **kwargs):
            raise requests.exceptions.Timeout("Connection timed out")
        return side_effect
<<<<<<< HEAD
    
    @staticmethod 
=======

    @staticmethod
>>>>>>> faace65 (Add comprehensive OAuth security, testing, and coverage infrastructure)
    def connection_error():
        """Simulate a connection error."""
        def side_effect(*args, **kwargs):
            raise requests.exceptions.ConnectionError("Failed to establish connection")
        return side_effect
<<<<<<< HEAD
    
=======

>>>>>>> faace65 (Add comprehensive OAuth security, testing, and coverage infrastructure)
    @staticmethod
    def http_error(status_code, response_data=None):
        """Simulate HTTP error response."""
        response_data = response_data or {"error": "server_error"}
<<<<<<< HEAD
        
=======

>>>>>>> faace65 (Add comprehensive OAuth security, testing, and coverage infrastructure)
        mock_response = Mock(spec=requests.Response)
        mock_response.status_code = status_code
        mock_response.json.return_value = response_data
        mock_response.text = json.dumps(response_data)
<<<<<<< HEAD
        
=======

>>>>>>> faace65 (Add comprehensive OAuth security, testing, and coverage infrastructure)
        if 400 <= status_code < 500:
            mock_response.raise_for_status.side_effect = requests.exceptions.HTTPError(f"{status_code} Client Error")
        elif status_code >= 500:
            mock_response.raise_for_status.side_effect = requests.exceptions.HTTPError(f"{status_code} Server Error")
<<<<<<< HEAD
            
        return mock_response
    
=======

        return mock_response

>>>>>>> faace65 (Add comprehensive OAuth security, testing, and coverage infrastructure)
    @staticmethod
    def malformed_json_response():
        """Simulate malformed JSON response."""
        mock_response = Mock(spec=requests.Response)
        mock_response.status_code = 200
        mock_response.json.side_effect = json.JSONDecodeError("Invalid JSON", "", 0)
        mock_response.text = "Invalid JSON content"
        return mock_response
<<<<<<< HEAD
    
=======

>>>>>>> faace65 (Add comprehensive OAuth security, testing, and coverage infrastructure)
    @staticmethod
    def rate_limit_response(retry_after=None):
        """Simulate rate limit response."""
        headers = {}
        if retry_after:
            headers['Retry-After'] = str(retry_after)
<<<<<<< HEAD
            
=======

>>>>>>> faace65 (Add comprehensive OAuth security, testing, and coverage infrastructure)
        mock_response = Mock(spec=requests.Response)
        mock_response.status_code = 429
        mock_response.headers = headers
        mock_response.json.return_value = {"error": "rate_limit_exceeded"}
        mock_response.text = '{"error": "rate_limit_exceeded"}'
        return mock_response

class ConfigurationErrorSimulator:
    """Utilities to simulate configuration errors."""
<<<<<<< HEAD
    
=======

>>>>>>> faace65 (Add comprehensive OAuth security, testing, and coverage infrastructure)
    @staticmethod
    def missing_config():
        """Return empty configuration."""
        return {}
<<<<<<< HEAD
    
=======

>>>>>>> faace65 (Add comprehensive OAuth security, testing, and coverage infrastructure)
    @staticmethod
    def incomplete_config():
        """Return configuration missing required fields."""
        return {
            "twitter": {
                "client_id": "test_id"
                # Missing client_secret and scope
            }
        }
<<<<<<< HEAD
    
=======

>>>>>>> faace65 (Add comprehensive OAuth security, testing, and coverage infrastructure)
    @staticmethod
    def invalid_config():
        """Return configuration with invalid values."""
        return {
            "twitter": {
                "client_id": "",  # Empty client_id
                "client_secret": "test_secret",
                "scope": None  # Invalid scope type
            }
        }

class OAuthErrorSimulator:
    """Utilities to simulate OAuth-specific errors."""
<<<<<<< HEAD
    
=======

>>>>>>> faace65 (Add comprehensive OAuth security, testing, and coverage infrastructure)
    @staticmethod
    def user_denied_error():
        """Simulate user denying authorization."""
        return {
            "error": "access_denied",
            "error_description": "The user denied the request"
        }
<<<<<<< HEAD
    
=======

>>>>>>> faace65 (Add comprehensive OAuth security, testing, and coverage infrastructure)
    @staticmethod
    def invalid_code_error():
        """Simulate invalid authorization code."""
        return {
<<<<<<< HEAD
            "error": "invalid_grant", 
            "error_description": "The provided authorization grant is invalid"
        }
    
=======
            "error": "invalid_grant",
            "error_description": "The provided authorization grant is invalid"
        }

>>>>>>> faace65 (Add comprehensive OAuth security, testing, and coverage infrastructure)
    @staticmethod
    def expired_code_error():
        """Simulate expired authorization code."""
        return {
            "error": "invalid_grant",
            "error_description": "The authorization code has expired"
        }
<<<<<<< HEAD
    
=======

>>>>>>> faace65 (Add comprehensive OAuth security, testing, and coverage infrastructure)
    @staticmethod
    def invalid_client_error():
        """Simulate invalid client credentials."""
        return {
            "error": "invalid_client",
            "error_description": "Client authentication failed"
        }
<<<<<<< HEAD
    
=======

>>>>>>> faace65 (Add comprehensive OAuth security, testing, and coverage infrastructure)
    @staticmethod
    def insufficient_scope_error():
        """Simulate insufficient scope permissions."""
        return {
            "error": "insufficient_scope",
            "error_description": "The request requires higher privileges"
        }
```

### Configuration Error Tests
```python
# oauth2_capture/tests/test_configuration_errors.py
from django.test import TestCase, RequestFactory, override_settings
from django.contrib.auth.models import User
from unittest.mock import patch

from oauth2_capture.views import initiate_oauth2
from oauth2_capture.services.oauth2 import OAuth2ProviderFactory
from .utils.error_simulation import ConfigurationErrorSimulator
from .fixtures import OAuthTestData

class ConfigurationErrorTests(TestCase):
<<<<<<< HEAD
    
    def setUp(self):
        self.factory = RequestFactory()
        self.user = OAuthTestData.create_test_user()
        
=======

    def setUp(self):
        self.factory = RequestFactory()
        self.user = OAuthTestData.create_test_user()

>>>>>>> faace65 (Add comprehensive OAuth security, testing, and coverage infrastructure)
    @override_settings(OAUTH2_CONFIG={})
    def test_missing_provider_configuration(self):
        """Test error when provider is not configured."""
        with self.assertRaises(ValueError) as context:
            OAuth2ProviderFactory.get_provider('twitter')
<<<<<<< HEAD
        
        self.assertIn('Unsupported provider', str(context.exception))
        
=======

        self.assertIn('Unsupported provider', str(context.exception))

>>>>>>> faace65 (Add comprehensive OAuth security, testing, and coverage infrastructure)
    @override_settings(OAUTH2_CONFIG=ConfigurationErrorSimulator.incomplete_config())
    def test_incomplete_provider_configuration(self):
        """Test error when provider configuration is incomplete."""
        request = self.factory.get('/oauth2/twitter/authorize/')
        request.user = self.user
<<<<<<< HEAD
        
=======

>>>>>>> faace65 (Add comprehensive OAuth security, testing, and coverage infrastructure)
        # Should handle missing configuration gracefully
        with self.assertRaises(KeyError):
            provider = OAuth2ProviderFactory.get_provider('twitter')
            provider.get_authorization_url('state', 'redirect_uri', request)
<<<<<<< HEAD
    
=======

>>>>>>> faace65 (Add comprehensive OAuth security, testing, and coverage infrastructure)
    @override_settings(OAUTH2_CONFIG=ConfigurationErrorSimulator.invalid_config())
    def test_invalid_configuration_values(self):
        """Test error when configuration has invalid values."""
        request = self.factory.get('/oauth2/twitter/authorize/')
        request.user = self.user
<<<<<<< HEAD
        
        provider = OAuth2ProviderFactory.get_provider('twitter')
        
        # Empty client_id should cause issues
        with self.assertRaises((ValueError, TypeError)):
            provider.get_authorization_url('state', 'redirect_uri', request)
    
=======

        provider = OAuth2ProviderFactory.get_provider('twitter')

        # Empty client_id should cause issues
        with self.assertRaises((ValueError, TypeError)):
            provider.get_authorization_url('state', 'redirect_uri', request)

>>>>>>> faace65 (Add comprehensive OAuth security, testing, and coverage infrastructure)
    def test_unsupported_provider_name(self):
        """Test error handling for unsupported provider names."""
        request = self.factory.get('/oauth2/unsupported/authorize/')
        request.user = self.user
<<<<<<< HEAD
        
        response = initiate_oauth2(request, 'unsupported')
        
=======

        response = initiate_oauth2(request, 'unsupported')

>>>>>>> faace65 (Add comprehensive OAuth security, testing, and coverage infrastructure)
        self.assertEqual(response.status_code, 400)
        self.assertIn('Unsupported provider', response.content.decode())
```

### Network Error Tests
```python
# oauth2_capture/tests/test_network_errors.py
from django.test import TestCase
from unittest.mock import patch, Mock
import requests

from oauth2_capture.services.oauth2 import TwitterOAuth2Provider
from oauth2_capture.models import OAuthToken
from .utils.error_simulation import NetworkErrorSimulator
from .fixtures import OAuthTestData

class NetworkErrorTests(TestCase):
<<<<<<< HEAD
    
    def setUp(self):
        self.provider = TwitterOAuth2Provider('twitter')
        self.user = OAuthTestData.create_test_user()
        
=======

    def setUp(self):
        self.provider = TwitterOAuth2Provider('twitter')
        self.user = OAuthTestData.create_test_user()

>>>>>>> faace65 (Add comprehensive OAuth security, testing, and coverage infrastructure)
    @patch('requests.post')
    def test_token_exchange_timeout(self, mock_post):
        """Test handling of network timeout during token exchange."""
        mock_post.side_effect = NetworkErrorSimulator.timeout_error()
<<<<<<< HEAD
        
=======

>>>>>>> faace65 (Add comprehensive OAuth security, testing, and coverage infrastructure)
        with self.assertRaises(requests.exceptions.Timeout):
            self.provider.exchange_code_for_token(
                code='test_code',
                redirect_uri='http://example.com/callback',
                request=Mock(session={'code_verifier': 'test_verifier'})
            )
<<<<<<< HEAD
    
    @patch('requests.post') 
    def test_token_exchange_connection_error(self, mock_post):
        """Test handling of connection error during token exchange."""
        mock_post.side_effect = NetworkErrorSimulator.connection_error()
        
        with self.assertRaises(requests.exceptions.ConnectionError):
            self.provider.exchange_code_for_token(
                code='test_code',
                redirect_uri='http://example.com/callback', 
                request=Mock(session={'code_verifier': 'test_verifier'})
            )
    
=======

    @patch('requests.post')
    def test_token_exchange_connection_error(self, mock_post):
        """Test handling of connection error during token exchange."""
        mock_post.side_effect = NetworkErrorSimulator.connection_error()

        with self.assertRaises(requests.exceptions.ConnectionError):
            self.provider.exchange_code_for_token(
                code='test_code',
                redirect_uri='http://example.com/callback',
                request=Mock(session={'code_verifier': 'test_verifier'})
            )

>>>>>>> faace65 (Add comprehensive OAuth security, testing, and coverage infrastructure)
    @patch('requests.post')
    def test_token_exchange_http_error(self, mock_post):
        """Test handling of HTTP error responses."""
        mock_post.return_value = NetworkErrorSimulator.http_error(
            status_code=500,
            response_data={"error": "internal_server_error"}
        )
<<<<<<< HEAD
        
=======

>>>>>>> faace65 (Add comprehensive OAuth security, testing, and coverage infrastructure)
        result = self.provider.exchange_code_for_token(
            code='test_code',
            redirect_uri='http://example.com/callback',
            request=Mock(session={'code_verifier': 'test_verifier'})
        )
<<<<<<< HEAD
        
        # Should return error response
        self.assertIn('error', result)
        self.assertEqual(result['error'], 'internal_server_error')
    
=======

        # Should return error response
        self.assertIn('error', result)
        self.assertEqual(result['error'], 'internal_server_error')

>>>>>>> faace65 (Add comprehensive OAuth security, testing, and coverage infrastructure)
    @patch('requests.get')
    def test_user_info_malformed_json(self, mock_get):
        """Test handling of malformed JSON in user info response."""
        mock_get.return_value = NetworkErrorSimulator.malformed_json_response()
<<<<<<< HEAD
        
        with self.assertRaises(ValueError):  # JSON decode error should be handled
            self.provider.get_user_info('test_token')
    
    @patch('requests.post')
    def test_rate_limiting_with_retry_after(self, mock_post):
        """Test handling of rate limit responses with Retry-After header.""" 
=======

        with self.assertRaises(ValueError):  # JSON decode error should be handled
            self.provider.get_user_info('test_token')

    @patch('requests.post')
    def test_rate_limiting_with_retry_after(self, mock_post):
        """Test handling of rate limit responses with Retry-After header."""
>>>>>>> faace65 (Add comprehensive OAuth security, testing, and coverage infrastructure)
        # First call returns rate limit, second succeeds
        mock_post.side_effect = [
            NetworkErrorSimulator.rate_limit_response(retry_after=5),
            NetworkErrorSimulator.http_error(200, {"access_token": "success"})
        ]
<<<<<<< HEAD
        
        # This tests the retry_with_backoff functionality
        with patch('time.sleep') as mock_sleep:
            result = self.provider.refresh_token('test_refresh_token')
            
            # Should have slept for retry delay
            mock_sleep.assert_called_with(5)  # Retry-After value
    
=======

        # This tests the retry_with_backoff functionality
        with patch('time.sleep') as mock_sleep:
            result = self.provider.refresh_token('test_refresh_token')

            # Should have slept for retry delay
            mock_sleep.assert_called_with(5)  # Retry-After value

>>>>>>> faace65 (Add comprehensive OAuth security, testing, and coverage infrastructure)
    @patch('requests.post')
    def test_refresh_token_network_error(self, mock_post):
        """Test refresh token failure due to network errors."""
        mock_post.side_effect = NetworkErrorSimulator.connection_error()
<<<<<<< HEAD
        
        token = OAuthTestData.create_test_token(self.user, expired=True)
        
        # Should handle network error gracefully
        result = self.provider.get_valid_token(token)
        
=======

        token = OAuthTestData.create_test_token(self.user, expired=True)

        # Should handle network error gracefully
        result = self.provider.get_valid_token(token)

>>>>>>> faace65 (Add comprehensive OAuth security, testing, and coverage infrastructure)
        # Should return None when refresh fails due to network error
        self.assertIsNone(result)
```

### OAuth Protocol Error Tests
```python
# oauth2_capture/tests/test_oauth_protocol_errors.py
from django.test import TestCase, RequestFactory
from django.contrib.sessions.middleware import SessionMiddleware
from unittest.mock import patch, Mock

from oauth2_capture.views import oauth2_callback
from oauth2_capture.models import OAuthToken
from .utils.error_simulation import OAuthErrorSimulator, NetworkErrorSimulator
from .fixtures import OAuthTestData

class OAuthProtocolErrorTests(TestCase):
<<<<<<< HEAD
    
    def setUp(self):
        self.factory = RequestFactory()
        self.user = OAuthTestData.create_test_user()
        
=======

    def setUp(self):
        self.factory = RequestFactory()
        self.user = OAuthTestData.create_test_user()

>>>>>>> faace65 (Add comprehensive OAuth security, testing, and coverage infrastructure)
    def add_session_to_request(self, request):
        """Add session support to request factory requests."""
        middleware = SessionMiddleware()
        middleware.process_request(request)
        request.session.save()
        return request
<<<<<<< HEAD
    
=======

>>>>>>> faace65 (Add comprehensive OAuth security, testing, and coverage infrastructure)
    def test_user_denied_authorization(self):
        """Test handling when user denies authorization."""
        request = self.factory.get(
            '/oauth2/twitter/callback/?error=access_denied&error_description=The+user+denied+the+request&state=test_state'
        )
        request.user = self.user
        request = self.add_session_to_request(request)
        request.session['twitter_oauth_state'] = 'test_state'
<<<<<<< HEAD
        
        response = oauth2_callback(request, 'twitter')
        
        # Should handle user denial gracefully
        self.assertEqual(response.status_code, 400)
        self.assertIn('denied', response.content.decode().lower())
    
=======

        response = oauth2_callback(request, 'twitter')

        # Should handle user denial gracefully
        self.assertEqual(response.status_code, 400)
        self.assertIn('denied', response.content.decode().lower())

>>>>>>> faace65 (Add comprehensive OAuth security, testing, and coverage infrastructure)
    @patch('requests.post')
    def test_invalid_authorization_code(self, mock_post):
        """Test handling of invalid authorization code."""
        mock_post.return_value = NetworkErrorSimulator.http_error(
            status_code=400,
            response_data=OAuthErrorSimulator.invalid_code_error()
        )
<<<<<<< HEAD
        
=======

>>>>>>> faace65 (Add comprehensive OAuth security, testing, and coverage infrastructure)
        request = self.factory.get('/oauth2/twitter/callback/?code=invalid_code&state=test_state')
        request.user = self.user
        request = self.add_session_to_request(request)
        request.session['twitter_oauth_state'] = 'test_state'
<<<<<<< HEAD
        
        response = oauth2_callback(request, 'twitter')
        
        self.assertEqual(response.status_code, 400)
        self.assertIn('Failed to connect', response.content.decode())
    
=======

        response = oauth2_callback(request, 'twitter')

        self.assertEqual(response.status_code, 400)
        self.assertIn('Failed to connect', response.content.decode())

>>>>>>> faace65 (Add comprehensive OAuth security, testing, and coverage infrastructure)
    @patch('requests.post')
    def test_expired_authorization_code(self, mock_post):
        """Test handling of expired authorization code."""
        mock_post.return_value = NetworkErrorSimulator.http_error(
            status_code=400,
            response_data=OAuthErrorSimulator.expired_code_error()
        )
<<<<<<< HEAD
        
=======

>>>>>>> faace65 (Add comprehensive OAuth security, testing, and coverage infrastructure)
        request = self.factory.get('/oauth2/twitter/callback/?code=expired_code&state=test_state')
        request.user = self.user
        request = self.add_session_to_request(request)
        request.session['twitter_oauth_state'] = 'test_state'
<<<<<<< HEAD
        
        response = oauth2_callback(request, 'twitter')
        
        self.assertEqual(response.status_code, 400)
        # Should indicate that the code was invalid/expired
        self.assertIn('Failed to connect', response.content.decode())
    
=======

        response = oauth2_callback(request, 'twitter')

        self.assertEqual(response.status_code, 400)
        # Should indicate that the code was invalid/expired
        self.assertIn('Failed to connect', response.content.decode())

>>>>>>> faace65 (Add comprehensive OAuth security, testing, and coverage infrastructure)
    @patch('requests.post')
    def test_invalid_client_credentials(self, mock_post):
        """Test handling of invalid client credentials."""
        mock_post.return_value = NetworkErrorSimulator.http_error(
            status_code=401,
            response_data=OAuthErrorSimulator.invalid_client_error()
        )
<<<<<<< HEAD
        
=======

>>>>>>> faace65 (Add comprehensive OAuth security, testing, and coverage infrastructure)
        request = self.factory.get('/oauth2/twitter/callback/?code=test_code&state=test_state')
        request.user = self.user
        request = self.add_session_to_request(request)
        request.session['twitter_oauth_state'] = 'test_state'
<<<<<<< HEAD
        
        response = oauth2_callback(request, 'twitter')
        
        self.assertEqual(response.status_code, 400)
        # This indicates a configuration problem
        
=======

        response = oauth2_callback(request, 'twitter')

        self.assertEqual(response.status_code, 400)
        # This indicates a configuration problem

>>>>>>> faace65 (Add comprehensive OAuth security, testing, and coverage infrastructure)
    def test_missing_authorization_code(self):
        """Test handling when no authorization code is provided."""
        request = self.factory.get('/oauth2/twitter/callback/?state=test_state')
        request.user = self.user
        request = self.add_session_to_request(request)
        request.session['twitter_oauth_state'] = 'test_state'
<<<<<<< HEAD
        
        response = oauth2_callback(request, 'twitter')
        
        self.assertEqual(response.status_code, 400)
        self.assertIn('Failed to connect', response.content.decode())
    
=======

        response = oauth2_callback(request, 'twitter')

        self.assertEqual(response.status_code, 400)
        self.assertIn('Failed to connect', response.content.decode())

>>>>>>> faace65 (Add comprehensive OAuth security, testing, and coverage infrastructure)
    def test_csrf_state_mismatch(self):
        """Test CSRF protection via state parameter verification."""
        request = self.factory.get('/oauth2/twitter/callback/?code=test_code&state=wrong_state')
        request.user = self.user
        request = self.add_session_to_request(request)
        request.session['twitter_oauth_state'] = 'correct_state'
<<<<<<< HEAD
        
        response = oauth2_callback(request, 'twitter')
        
        # Should reject due to state mismatch
        self.assertEqual(response.status_code, 400)
    
    def test_missing_state_parameter(self):
        """Test handling when state parameter is missing entirely.""" 
=======

        response = oauth2_callback(request, 'twitter')

        # Should reject due to state mismatch
        self.assertEqual(response.status_code, 400)

    def test_missing_state_parameter(self):
        """Test handling when state parameter is missing entirely."""
>>>>>>> faace65 (Add comprehensive OAuth security, testing, and coverage infrastructure)
        request = self.factory.get('/oauth2/twitter/callback/?code=test_code')
        request.user = self.user
        request = self.add_session_to_request(request)
        request.session['twitter_oauth_state'] = 'test_state'
<<<<<<< HEAD
        
        response = oauth2_callback(request, 'twitter')
        
=======

        response = oauth2_callback(request, 'twitter')

>>>>>>> faace65 (Add comprehensive OAuth security, testing, and coverage infrastructure)
        # Should reject due to missing state
        self.assertEqual(response.status_code, 400)
```

### Token Lifecycle Error Tests
```python
# oauth2_capture/tests/test_token_errors.py
from django.test import TestCase
from django.utils import timezone
from datetime import timedelta
from unittest.mock import patch, Mock
import requests

from oauth2_capture.services.oauth2 import TwitterOAuth2Provider
from oauth2_capture.models import OAuthToken
from .utils.error_simulation import NetworkErrorSimulator, OAuthErrorSimulator
from .fixtures import OAuthTestData

class TokenErrorTests(TestCase):
<<<<<<< HEAD
    
    def setUp(self):
        self.provider = TwitterOAuth2Provider('twitter')
        self.user = OAuthTestData.create_test_user()
        
=======

    def setUp(self):
        self.provider = TwitterOAuth2Provider('twitter')
        self.user = OAuthTestData.create_test_user()

>>>>>>> faace65 (Add comprehensive OAuth security, testing, and coverage infrastructure)
    @patch('requests.post')
    def test_refresh_token_expired(self, mock_post):
        """Test handling when refresh token itself has expired."""
        mock_post.return_value = NetworkErrorSimulator.http_error(
            status_code=400,
            response_data={"error": "invalid_grant", "error_description": "Refresh token expired"}
        )
<<<<<<< HEAD
        
        # Create expired token
        token = OAuthTestData.create_test_token(self.user, expired=True)
        
        result = self.provider.get_valid_token(token)
        
        # Should return None when refresh fails
        self.assertIsNone(result)
        
=======

        # Create expired token
        token = OAuthTestData.create_test_token(self.user, expired=True)

        result = self.provider.get_valid_token(token)

        # Should return None when refresh fails
        self.assertIsNone(result)

>>>>>>> faace65 (Add comprehensive OAuth security, testing, and coverage infrastructure)
    @patch('requests.post')
    def test_token_revoked_by_user(self, mock_post):
        """Test handling when user has revoked token permissions."""
        mock_post.return_value = NetworkErrorSimulator.http_error(
            status_code=401,
            response_data={"error": "invalid_grant", "error_description": "Token revoked"}
        )
<<<<<<< HEAD
        
        token = OAuthTestData.create_test_token(self.user, expired=True)
        
        result = self.provider.get_valid_token(token)
        
        # Should return None for revoked tokens
        self.assertIsNone(result)
    
    def test_token_not_expired_but_invalid(self):
        """Test token that appears valid but is actually invalid."""
        token = OAuthTestData.create_test_token(self.user, expired=False)
        
        # Token appears valid locally but may be revoked remotely
        # This would be caught when actually making API calls
        self.assertFalse(token.is_expired)
    
=======

        token = OAuthTestData.create_test_token(self.user, expired=True)

        result = self.provider.get_valid_token(token)

        # Should return None for revoked tokens
        self.assertIsNone(result)

    def test_token_not_expired_but_invalid(self):
        """Test token that appears valid but is actually invalid."""
        token = OAuthTestData.create_test_token(self.user, expired=False)

        # Token appears valid locally but may be revoked remotely
        # This would be caught when actually making API calls
        self.assertFalse(token.is_expired)

>>>>>>> faace65 (Add comprehensive OAuth security, testing, and coverage infrastructure)
    @patch('requests.post')
    def test_partial_refresh_response(self, mock_post):
        """Test handling of incomplete refresh token response."""
        # Response missing required fields
        mock_post.return_value = Mock(
            status_code=200,
            json=lambda: {"token_type": "bearer"}  # Missing access_token
        )
<<<<<<< HEAD
        
        token = OAuthTestData.create_test_token(self.user, expired=True)
        
        result = self.provider.get_valid_token(token)
        
        # Should return None for incomplete responses
        self.assertIsNone(result)
    
=======

        token = OAuthTestData.create_test_token(self.user, expired=True)

        result = self.provider.get_valid_token(token)

        # Should return None for incomplete responses
        self.assertIsNone(result)

>>>>>>> faace65 (Add comprehensive OAuth security, testing, and coverage infrastructure)
    @patch('oauth2_capture.services.oauth2.OAuth2Provider.update_token')
    def test_token_update_database_error(self, mock_update):
        """Test handling of database errors during token updates."""
        from django.db import IntegrityError
<<<<<<< HEAD
        
        mock_update.side_effect = IntegrityError("Database constraint violation")
        
        token = OAuthTestData.create_test_token(self.user, expired=True)
        
=======

        mock_update.side_effect = IntegrityError("Database constraint violation")

        token = OAuthTestData.create_test_token(self.user, expired=True)

>>>>>>> faace65 (Add comprehensive OAuth security, testing, and coverage infrastructure)
        # Should handle database errors gracefully
        with patch('requests.post') as mock_post:
            mock_post.return_value = Mock(
                status_code=200,
                json=lambda: {"access_token": "new_token", "expires_in": 3600}
            )
<<<<<<< HEAD
            
            result = self.provider.get_valid_token(token)
            
=======

            result = self.provider.get_valid_token(token)

>>>>>>> faace65 (Add comprehensive OAuth security, testing, and coverage infrastructure)
            # Should return None when database update fails
            self.assertIsNone(result)
```

## Success Criteria
- [ ] Comprehensive error scenario coverage for all failure points
- [ ] Realistic error simulation using proper mock techniques
- [ ] Graceful error handling verification
- [ ] Error logging verification
- [ ] Error message quality validation
- [ ] Network resilience testing
- [ ] Protocol compliance verification
<<<<<<< HEAD
- [ ] Edge case and race condition testing
=======
- [ ] Edge case and race condition testing
>>>>>>> faace65 (Add comprehensive OAuth security, testing, and coverage infrastructure)
