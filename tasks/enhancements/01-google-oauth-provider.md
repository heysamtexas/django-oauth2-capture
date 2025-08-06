# Google OAuth Provider Implementation

## Objective
Implement Google OAuth 2.0 provider support for the oauth2_capture library, enabling access to Google services like Gmail, Google Drive, YouTube, Google Calendar, and other Google APIs.

## Context
Google OAuth 2.0 was identified as a high-priority provider during our discussion. Google's OAuth implementation provides access to a wide range of services and has a large user base, making it valuable for many applications.

**Google OAuth 2.0 Characteristics:**
- Standard OAuth 2.0 flow (no PKCE requirement for web apps)
- Short-lived access tokens (1 hour)
- Refresh tokens for long-term access
- Extensive scope system for different Google services
- Well-documented APIs with good error handling

**Key Considerations:**
- Multiple service integration (Gmail, Drive, Calendar, etc.)
- Granular scope permissions
- Google Identity verification requirements for sensitive scopes
- Rate limiting across different Google APIs
- User consent screen configuration

**Integration Benefits:**
- Access to Google Workspace APIs
- Calendar and email integration
- File storage and sharing (Drive)
- YouTube content management
- Google Analytics and other business APIs

## Technical Details

### Google OAuth 2.0 Implementation

Google OAuth follows the standard OAuth 2.0 flow with these specifics:

1. **Authorization Endpoint**: `https://accounts.google.com/o/oauth2/v2/auth`
2. **Token Endpoint**: `https://oauth2.googleapis.com/token`
3. **User Info Endpoint**: `https://www.googleapis.com/oauth2/v2/userinfo`
4. **Token Validation**: `https://www.googleapis.com/oauth2/v1/tokeninfo`

### Scope Categories

Google uses hierarchical scopes:
- **Profile/Email**: Basic user information
- **Gmail**: Email access and management
- **Drive**: File storage and sharing
- **Calendar**: Calendar events and management
- **YouTube**: Video and channel management
- **Analytics**: Website and app analytics

### Implementation Requirements

1. **Provider Class**: Implement `GoogleOAuth2Provider` extending `OAuth2Provider`
2. **Scope Management**: Handle Google's extensive scope system
3. **Service Detection**: Detect which Google services are accessible
4. **Error Handling**: Handle Google-specific error responses
5. **Rate Limiting**: Respect Google API quotas and limits

## Testing Requirements
1. **OAuth Flow Tests**: Authorization, token exchange, refresh
2. **API Integration Tests**: Test actual Google API calls
3. **Scope Permission Tests**: Verify different scope combinations
4. **Error Handling Tests**: Test Google-specific error scenarios
5. **Rate Limiting Tests**: Test quota and rate limit handling
6. **Multi-Service Tests**: Test access to different Google services

## Dependencies
- Core OAuth flow tests (testing task 01)
- Provider-specific tests framework (testing task 02)
- Google API credentials for testing
- Understanding of Google's developer console and app verification process

## Estimated Complexity
Medium (1 day)

## Files to Create/Modify
- `oauth2_capture/services/oauth2.py`: Add `GoogleOAuth2Provider` class
- `oauth2_capture/tests/providers/test_google.py`: Comprehensive Google provider tests
- `oauth2_capture/tests/providers/mock_responses.py`: Add Google API response mocks
- `docs/google-setup.md`: Google OAuth setup documentation
- `development/development/settings.py`: Add Google configuration example

## Example Implementation

### Google OAuth Provider Class
```python
# Addition to oauth2_capture/services/oauth2.py

class GoogleOAuth2Provider(OAuth2Provider):
    """Google OAuth2 provider with multi-service support."""
<<<<<<< HEAD
    
=======

>>>>>>> faace65 (Add comprehensive OAuth security, testing, and coverage infrastructure)
    @property
    def authorize_url(self) -> str:
        """The URL to authorize the user."""
        return "https://accounts.google.com/o/oauth2/v2/auth"
<<<<<<< HEAD
    
=======

>>>>>>> faace65 (Add comprehensive OAuth security, testing, and coverage infrastructure)
    @property
    def token_url(self) -> str:
        """The URL to exchange the code for a token."""
        return "https://oauth2.googleapis.com/token"
<<<<<<< HEAD
    
=======

>>>>>>> faace65 (Add comprehensive OAuth security, testing, and coverage infrastructure)
    @property
    def user_info_url(self) -> str:
        """The URL to get the user info."""
        return "https://www.googleapis.com/oauth2/v2/userinfo"
<<<<<<< HEAD
    
=======

>>>>>>> faace65 (Add comprehensive OAuth security, testing, and coverage infrastructure)
    def get_authorization_url(self, state: str, redirect_uri: str, request: HttpRequest) -> str:
        """Get the authorization URL with Google-specific parameters."""
        params = {
            "client_id": self.config["client_id"],
            "redirect_uri": redirect_uri,
            "response_type": "code",
            "state": state,
            "scope": self.config["scope"],
            "access_type": "offline",  # Required for refresh tokens
            "prompt": "consent",  # Ensure refresh token is always returned
        }
<<<<<<< HEAD
        
        # Add optional parameters
        if "include_granted_scopes" in self.config:
            params["include_granted_scopes"] = self.config["include_granted_scopes"]
        
        return f"{self.authorize_url}?{urlencode(params)}"
    
    def get_user_info(self, access_token: str) -> dict:
        """Get the user info from Google."""
        headers = {"Authorization": f"Bearer {access_token}"}
        
        try:
            response = requests.get(self.user_info_url, headers=headers, timeout=10)
            response.raise_for_status()
            
            user_data = response.json()
            
            # Enhance with additional Google-specific info
            user_data = self._enhance_user_data(user_data, access_token)
            
            return user_data
            
        except requests.exceptions.RequestException as e:
            logger.error("Google user info request failed: %s", str(e))
            raise
    
    def _enhance_user_data(self, user_data: dict, access_token: str) -> dict:
        """Enhance user data with additional Google information."""
        
        # Add accessible services based on scopes
        user_data["accessible_services"] = self._detect_accessible_services(access_token)
        
        # Add Google-specific fields mapping
        user_data["username"] = user_data.get("email", "").split("@")[0]
        user_data["avatar_url"] = user_data.get("picture")
        
        return user_data
    
    def _detect_accessible_services(self, access_token: str) -> list:
        """Detect which Google services are accessible with current token."""
        services = []
        
        # Map scopes to services
        scope_service_map = {
            "https://www.googleapis.com/auth/gmail": "gmail",
            "https://www.googleapis.com/auth/drive": "drive", 
=======

        # Add optional parameters
        if "include_granted_scopes" in self.config:
            params["include_granted_scopes"] = self.config["include_granted_scopes"]

        return f"{self.authorize_url}?{urlencode(params)}"

    def get_user_info(self, access_token: str) -> dict:
        """Get the user info from Google."""
        headers = {"Authorization": f"Bearer {access_token}"}

        try:
            response = requests.get(self.user_info_url, headers=headers, timeout=10)
            response.raise_for_status()

            user_data = response.json()

            # Enhance with additional Google-specific info
            user_data = self._enhance_user_data(user_data, access_token)

            return user_data

        except requests.exceptions.RequestException as e:
            logger.error("Google user info request failed: %s", str(e))
            raise

    def _enhance_user_data(self, user_data: dict, access_token: str) -> dict:
        """Enhance user data with additional Google information."""

        # Add accessible services based on scopes
        user_data["accessible_services"] = self._detect_accessible_services(access_token)

        # Add Google-specific fields mapping
        user_data["username"] = user_data.get("email", "").split("@")[0]
        user_data["avatar_url"] = user_data.get("picture")

        return user_data

    def _detect_accessible_services(self, access_token: str) -> list:
        """Detect which Google services are accessible with current token."""
        services = []

        # Map scopes to services
        scope_service_map = {
            "https://www.googleapis.com/auth/gmail": "gmail",
            "https://www.googleapis.com/auth/drive": "drive",
>>>>>>> faace65 (Add comprehensive OAuth security, testing, and coverage infrastructure)
            "https://www.googleapis.com/auth/calendar": "calendar",
            "https://www.googleapis.com/auth/youtube": "youtube",
            "https://www.googleapis.com/auth/analytics": "analytics",
            "https://www.googleapis.com/auth/contacts": "contacts",
        }
<<<<<<< HEAD
        
=======

>>>>>>> faace65 (Add comprehensive OAuth security, testing, and coverage infrastructure)
        # Check token info to see granted scopes
        try:
            token_info = self._get_token_info(access_token)
            granted_scopes = token_info.get("scope", "").split()
<<<<<<< HEAD
            
            for scope in granted_scopes:
                if scope in scope_service_map:
                    services.append(scope_service_map[scope])
                    
        except Exception as e:
            logger.debug("Could not detect Google services: %s", str(e))
        
        return services
    
=======

            for scope in granted_scopes:
                if scope in scope_service_map:
                    services.append(scope_service_map[scope])

        except Exception as e:
            logger.debug("Could not detect Google services: %s", str(e))

        return services

>>>>>>> faace65 (Add comprehensive OAuth security, testing, and coverage infrastructure)
    def _get_token_info(self, access_token: str) -> dict:
        """Get token information from Google."""
        url = "https://www.googleapis.com/oauth2/v1/tokeninfo"
        params = {"access_token": access_token}
<<<<<<< HEAD
        
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        
        return response.json()
    
=======

        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()

        return response.json()

>>>>>>> faace65 (Add comprehensive OAuth security, testing, and coverage infrastructure)
    def exchange_code_for_token(self, code: str, redirect_uri: str, request: HttpRequest) -> dict:
        """Exchange the auth code for an access token."""
        data = {
            "grant_type": "authorization_code",
            "code": code,
            "redirect_uri": redirect_uri,
            "client_id": self.config["client_id"],
            "client_secret": self.config["client_secret"],
        }
<<<<<<< HEAD
        
        headers = {"Content-Type": "application/x-www-form-urlencoded"}
        
        try:
            response = requests.post(self.token_url, data=data, headers=headers, timeout=10)
            response.raise_for_status()
            
            token_data = response.json()
            
            # Log successful token exchange
            logger.info("Google token exchange successful for redirect_uri: %s", redirect_uri)
            
            return token_data
            
        except requests.exceptions.RequestException as e:
            logger.error("Google token exchange failed: %s", str(e))
            
=======

        headers = {"Content-Type": "application/x-www-form-urlencoded"}

        try:
            response = requests.post(self.token_url, data=data, headers=headers, timeout=10)
            response.raise_for_status()

            token_data = response.json()

            # Log successful token exchange
            logger.info("Google token exchange successful for redirect_uri: %s", redirect_uri)

            return token_data

        except requests.exceptions.RequestException as e:
            logger.error("Google token exchange failed: %s", str(e))

>>>>>>> faace65 (Add comprehensive OAuth security, testing, and coverage infrastructure)
            # Return error information for better debugging
            if hasattr(e, 'response') and e.response is not None:
                try:
                    error_data = e.response.json()
                    return error_data
                except ValueError:
                    return {"error": "token_exchange_failed", "error_description": str(e)}
<<<<<<< HEAD
            
            return {"error": "network_error", "error_description": str(e)}
    
=======

            return {"error": "network_error", "error_description": str(e)}

>>>>>>> faace65 (Add comprehensive OAuth security, testing, and coverage infrastructure)
    def refresh_token(self, refresh_token: str) -> dict:
        """Refresh the Google access token."""
        data = {
            "grant_type": "refresh_token",
            "refresh_token": refresh_token,
            "client_id": self.config["client_id"],
            "client_secret": self.config["client_secret"],
        }
<<<<<<< HEAD
        
        headers = {"Content-Type": "application/x-www-form-urlencoded"}
        
        def do_request() -> requests.Response:
            return requests.post(self.token_url, data=data, headers=headers, timeout=10)
        
        response = retry_with_backoff(do_request)
        
=======

        headers = {"Content-Type": "application/x-www-form-urlencoded"}

        def do_request() -> requests.Response:
            return requests.post(self.token_url, data=data, headers=headers, timeout=10)

        response = retry_with_backoff(do_request)

>>>>>>> faace65 (Add comprehensive OAuth security, testing, and coverage infrastructure)
        if response.status_code == 200:
            token_data = response.json()
            logger.info("Google token refresh successful")
            return token_data
        else:
            logger.error("Google token refresh failed: %s - %s", response.status_code, response.text)
<<<<<<< HEAD
            
=======

>>>>>>> faace65 (Add comprehensive OAuth security, testing, and coverage infrastructure)
            try:
                error_data = response.json()
                return error_data
            except ValueError:
                return {"error": "refresh_failed", "error_description": response.text}
<<<<<<< HEAD
    
=======

>>>>>>> faace65 (Add comprehensive OAuth security, testing, and coverage infrastructure)
    def validate_token_detailed(self, access_token: str) -> 'TokenValidationResult':
        """Validate Google token with detailed information."""
        try:
            token_info = self._get_token_info(access_token)
<<<<<<< HEAD
            
=======

>>>>>>> faace65 (Add comprehensive OAuth security, testing, and coverage infrastructure)
            # Check if token is valid
            if "error" in token_info:
                return TokenValidationResult(
                    status=TokenValidationStatus.INVALID,
                    message=f"Token validation failed: {token_info.get('error_description', 'Unknown error')}",
                    provider=self.provider_name
                )
<<<<<<< HEAD
            
=======

>>>>>>> faace65 (Add comprehensive OAuth security, testing, and coverage infrastructure)
            # Check token expiration
            expires_in = token_info.get("expires_in")
            if expires_in and int(expires_in) <= 0:
                return TokenValidationResult(
                    status=TokenValidationStatus.EXPIRED,
                    message="Google token has expired",
                    provider=self.provider_name
                )
<<<<<<< HEAD
            
=======

>>>>>>> faace65 (Add comprehensive OAuth security, testing, and coverage infrastructure)
            return TokenValidationResult(
                status=TokenValidationStatus.VALID,
                message="Google token is valid",
                provider=self.provider_name,
                user_id=token_info.get("user_id"),
                scopes=token_info.get("scope", "").split(),
                expires_at=timezone.now() + timedelta(seconds=int(expires_in)) if expires_in else None
            )
<<<<<<< HEAD
            
=======

>>>>>>> faace65 (Add comprehensive OAuth security, testing, and coverage infrastructure)
        except requests.exceptions.RequestException as e:
            return TokenValidationResult(
                status=TokenValidationStatus.UNKNOWN,
                message=f"Token validation network error: {str(e)}",
                provider=self.provider_name
            )
<<<<<<< HEAD
    
=======

>>>>>>> faace65 (Add comprehensive OAuth security, testing, and coverage infrastructure)
    def get_service_client(self, oauth_token: 'OAuthToken', service_name: str):
        """Get a configured Google API service client."""
        # This would return configured Google API client libraries
        # Implementation would depend on specific Google client library usage
        access_token = self.get_valid_token(oauth_token)
<<<<<<< HEAD
        
        if not access_token:
            raise ValueError("No valid access token available")
        
=======

        if not access_token:
            raise ValueError("No valid access token available")

>>>>>>> faace65 (Add comprehensive OAuth security, testing, and coverage infrastructure)
        # Example structure - actual implementation would use Google client libraries
        return {
            'service': service_name,
            'access_token': access_token,
            'credentials': self._create_credentials(access_token)
        }
<<<<<<< HEAD
    
=======

>>>>>>> faace65 (Add comprehensive OAuth security, testing, and coverage infrastructure)
    def _create_credentials(self, access_token: str):
        """Create Google API credentials object."""
        # This would create proper Google credentials object
        # Placeholder for actual Google client library integration
        return {
            'token': access_token,
            'type': 'Bearer'
        }

# Update the factory to include Google
class OAuth2ProviderFactory:
    @staticmethod
    def get_provider(provider_name: str) -> OAuth2Provider:
        providers = {
            "twitter": TwitterOAuth2Provider,
            "linkedin": LinkedInOAuth2Provider,
            "github": GitHubOAuth2Provider,
            "reddit": RedditOAuth2Provider,
            "pinterest": PinterestOAuth2Provider,
            "facebook": FacebookOAuth2Provider,
            "google": GoogleOAuth2Provider,  # Add Google provider
        }
        provider_class = providers.get(provider_name)
        if not provider_class:
            msg = f"Unsupported provider: {provider_name}"
            raise ValueError(msg)
        return provider_class(provider_name)
```

### Google API Mock Responses
```python
# Addition to oauth2_capture/tests/providers/mock_responses.py

class GoogleMockResponses:
    """Google API response mocks."""
<<<<<<< HEAD
    
=======

>>>>>>> faace65 (Add comprehensive OAuth security, testing, and coverage infrastructure)
    TOKEN_EXCHANGE_SUCCESS = {
        "access_token": "ya29.a0AfH6SMBxxx...",
        "expires_in": 3599,
        "refresh_token": "1//04xxx...",
        "scope": "https://www.googleapis.com/auth/userinfo.email https://www.googleapis.com/auth/userinfo.profile openid",
        "token_type": "Bearer",
        "id_token": "eyJhbGciOiJSUzI1NiIsImtpZCI6Ijk1ZTAzZT..."
    }
<<<<<<< HEAD
    
=======

>>>>>>> faace65 (Add comprehensive OAuth security, testing, and coverage infrastructure)
    TOKEN_REFRESH_SUCCESS = {
        "access_token": "ya29.a0AfH6SMCxxx...",
        "expires_in": 3599,
        "scope": "https://www.googleapis.com/auth/userinfo.email https://www.googleapis.com/auth/userinfo.profile openid",
        "token_type": "Bearer"
    }
<<<<<<< HEAD
    
=======

>>>>>>> faace65 (Add comprehensive OAuth security, testing, and coverage infrastructure)
    USER_INFO_SUCCESS = {
        "id": "12345678901234567890",
        "email": "user@example.com",
        "verified_email": True,
        "name": "John Doe",
        "given_name": "John",
        "family_name": "Doe",
        "picture": "https://lh3.googleusercontent.com/a-/AOh14GhRxxx",
        "locale": "en"
    }
<<<<<<< HEAD
    
=======

>>>>>>> faace65 (Add comprehensive OAuth security, testing, and coverage infrastructure)
    TOKEN_INFO_SUCCESS = {
        "issued_to": "1234567890-xxx.apps.googleusercontent.com",
        "audience": "1234567890-xxx.apps.googleusercontent.com",
        "user_id": "12345678901234567890",
        "scope": "https://www.googleapis.com/auth/userinfo.email https://www.googleapis.com/auth/userinfo.profile openid",
        "expires_in": 3580,
        "email": "user@example.com",
        "verified_email": "true",
        "access_type": "offline"
    }
<<<<<<< HEAD
    
=======

>>>>>>> faace65 (Add comprehensive OAuth security, testing, and coverage infrastructure)
    TOKEN_EXCHANGE_ERROR = {
        "error": "invalid_grant",
        "error_description": "Bad Request"
    }
<<<<<<< HEAD
    
=======

>>>>>>> faace65 (Add comprehensive OAuth security, testing, and coverage infrastructure)
    TOKEN_INFO_INVALID = {
        "error": "invalid_token",
        "error_description": "Invalid Value"
    }
```

### Google Provider Tests
```python
# oauth2_capture/tests/providers/test_google.py
from django.test import TestCase, RequestFactory
from unittest.mock import patch, Mock
import json

from oauth2_capture.services.oauth2 import GoogleOAuth2Provider
from oauth2_capture.models import OAuthToken
from ..fixtures import OAuthTestData
from .mock_responses import GoogleMockResponses

class GoogleProviderTests(TestCase):
<<<<<<< HEAD
    
=======

>>>>>>> faace65 (Add comprehensive OAuth security, testing, and coverage infrastructure)
    def setUp(self):
        self.provider = GoogleOAuth2Provider('google')
        self.factory = RequestFactory()
        self.user = OAuthTestData.create_test_user()
<<<<<<< HEAD
    
    def test_authorization_url_parameters(self):
        """Test Google authorization URL contains correct parameters."""
        request = self.factory.get('/')
        
=======

    def test_authorization_url_parameters(self):
        """Test Google authorization URL contains correct parameters."""
        request = self.factory.get('/')

>>>>>>> faace65 (Add comprehensive OAuth security, testing, and coverage infrastructure)
        auth_url = self.provider.get_authorization_url(
            state='test_state',
            redirect_uri='http://example.com/callback',
            request=request
        )
<<<<<<< HEAD
        
        # Check base URL
        self.assertIn('https://accounts.google.com/o/oauth2/v2/auth', auth_url)
        
=======

        # Check base URL
        self.assertIn('https://accounts.google.com/o/oauth2/v2/auth', auth_url)

>>>>>>> faace65 (Add comprehensive OAuth security, testing, and coverage infrastructure)
        # Check required parameters
        self.assertIn('client_id=', auth_url)
        self.assertIn('redirect_uri=', auth_url)
        self.assertIn('response_type=code', auth_url)
        self.assertIn('state=test_state', auth_url)
        self.assertIn('scope=', auth_url)
<<<<<<< HEAD
        
        # Check Google-specific parameters
        self.assertIn('access_type=offline', auth_url)
        self.assertIn('prompt=consent', auth_url)
    
=======

        # Check Google-specific parameters
        self.assertIn('access_type=offline', auth_url)
        self.assertIn('prompt=consent', auth_url)

>>>>>>> faace65 (Add comprehensive OAuth security, testing, and coverage infrastructure)
    @patch('requests.post')
    def test_token_exchange_success(self, mock_post):
        """Test successful Google token exchange."""
        mock_post.return_value = Mock(
            status_code=200,
            json=lambda: GoogleMockResponses.TOKEN_EXCHANGE_SUCCESS,
            raise_for_status=lambda: None
        )
<<<<<<< HEAD
        
        request = self.factory.get('/')
        
=======

        request = self.factory.get('/')

>>>>>>> faace65 (Add comprehensive OAuth security, testing, and coverage infrastructure)
        result = self.provider.exchange_code_for_token(
            code='test_code',
            redirect_uri='http://example.com/callback',
            request=request
        )
<<<<<<< HEAD
        
        # Should call token endpoint
        mock_post.assert_called_once()
        call_args = mock_post.call_args
        
=======

        # Should call token endpoint
        mock_post.assert_called_once()
        call_args = mock_post.call_args

>>>>>>> faace65 (Add comprehensive OAuth security, testing, and coverage infrastructure)
        # Check data includes required fields
        self.assertIn('grant_type', call_args[1]['data'])
        self.assertEqual(call_args[1]['data']['grant_type'], 'authorization_code')
        self.assertIn('code', call_args[1]['data'])
        self.assertIn('client_id', call_args[1]['data'])
        self.assertIn('client_secret', call_args[1]['data'])
<<<<<<< HEAD
        
        # Check response parsing
        self.assertEqual(result['access_token'], GoogleMockResponses.TOKEN_EXCHANGE_SUCCESS['access_token'])
        self.assertIn('refresh_token', result)
    
=======

        # Check response parsing
        self.assertEqual(result['access_token'], GoogleMockResponses.TOKEN_EXCHANGE_SUCCESS['access_token'])
        self.assertIn('refresh_token', result)

>>>>>>> faace65 (Add comprehensive OAuth security, testing, and coverage infrastructure)
    @patch('requests.get')
    def test_user_info_retrieval(self, mock_get):
        """Test Google user info retrieval and enhancement."""
        # Mock token info call first
        mock_get.side_effect = [
            Mock(
                status_code=200,
                json=lambda: GoogleMockResponses.USER_INFO_SUCCESS,
                raise_for_status=lambda: None
            ),
            Mock(
                status_code=200,
                json=lambda: GoogleMockResponses.TOKEN_INFO_SUCCESS,
                raise_for_status=lambda: None
            )
        ]
<<<<<<< HEAD
        
        result = self.provider.get_user_info('test_token')
        
        # Should make two calls: user info and token info
        self.assertEqual(mock_get.call_count, 2)
        
=======

        result = self.provider.get_user_info('test_token')

        # Should make two calls: user info and token info
        self.assertEqual(mock_get.call_count, 2)

>>>>>>> faace65 (Add comprehensive OAuth security, testing, and coverage infrastructure)
        # Check enhanced data
        self.assertEqual(result['email'], GoogleMockResponses.USER_INFO_SUCCESS['email'])
        self.assertIn('accessible_services', result)
        self.assertIn('username', result)
        self.assertIn('avatar_url', result)
<<<<<<< HEAD
    
=======

>>>>>>> faace65 (Add comprehensive OAuth security, testing, and coverage infrastructure)
    @patch('requests.post')
    def test_token_refresh(self, mock_post):
        """Test Google token refresh."""
        mock_post.return_value = Mock(
            status_code=200,
            json=lambda: GoogleMockResponses.TOKEN_REFRESH_SUCCESS,
            raise_for_status=lambda: None
        )
<<<<<<< HEAD
        
        result = self.provider.refresh_token('test_refresh_token')
        
        # Should call token endpoint
        mock_post.assert_called_once()
        call_args = mock_post.call_args
        
        # Check refresh token data
        self.assertEqual(call_args[1]['data']['grant_type'], 'refresh_token')
        self.assertEqual(call_args[1]['data']['refresh_token'], 'test_refresh_token')
        
        # Check response
        self.assertEqual(result['access_token'], GoogleMockResponses.TOKEN_REFRESH_SUCCESS['access_token'])
    
=======

        result = self.provider.refresh_token('test_refresh_token')

        # Should call token endpoint
        mock_post.assert_called_once()
        call_args = mock_post.call_args

        # Check refresh token data
        self.assertEqual(call_args[1]['data']['grant_type'], 'refresh_token')
        self.assertEqual(call_args[1]['data']['refresh_token'], 'test_refresh_token')

        # Check response
        self.assertEqual(result['access_token'], GoogleMockResponses.TOKEN_REFRESH_SUCCESS['access_token'])

>>>>>>> faace65 (Add comprehensive OAuth security, testing, and coverage infrastructure)
    @patch('requests.get')
    def test_token_validation(self, mock_get):
        """Test Google token validation."""
        mock_get.return_value = Mock(
            status_code=200,
            json=lambda: GoogleMockResponses.TOKEN_INFO_SUCCESS,
            raise_for_status=lambda: None
        )
<<<<<<< HEAD
        
        result = self.provider.validate_token_detailed('test_token')
        
        # Should call token info endpoint
        mock_get.assert_called_once()
        
=======

        result = self.provider.validate_token_detailed('test_token')

        # Should call token info endpoint
        mock_get.assert_called_once()

>>>>>>> faace65 (Add comprehensive OAuth security, testing, and coverage infrastructure)
        # Check validation result
        from oauth2_capture.services.oauth2 import TokenValidationStatus
        self.assertEqual(result.status, TokenValidationStatus.VALID)
        self.assertEqual(result.provider, 'google')
        self.assertIsNotNone(result.scopes)
<<<<<<< HEAD
    
=======

>>>>>>> faace65 (Add comprehensive OAuth security, testing, and coverage infrastructure)
    @patch('requests.get')
    def test_accessible_services_detection(self, mock_get):
        """Test detection of accessible Google services."""
        mock_get.return_value = Mock(
            status_code=200,
            json=lambda: {
                **GoogleMockResponses.TOKEN_INFO_SUCCESS,
                "scope": "https://www.googleapis.com/auth/gmail.readonly https://www.googleapis.com/auth/drive https://www.googleapis.com/auth/userinfo.email"
            },
            raise_for_status=lambda: None
        )
<<<<<<< HEAD
        
        services = self.provider._detect_accessible_services('test_token')
        
=======

        services = self.provider._detect_accessible_services('test_token')

>>>>>>> faace65 (Add comprehensive OAuth security, testing, and coverage infrastructure)
        # Should detect Gmail and Drive services
        self.assertIn('gmail', services)
        self.assertIn('drive', services)
        self.assertNotIn('calendar', services)  # Not in scope
<<<<<<< HEAD
    
=======

>>>>>>> faace65 (Add comprehensive OAuth security, testing, and coverage infrastructure)
    @patch('requests.post')
    def test_error_handling(self, mock_post):
        """Test Google API error handling."""
        mock_post.return_value = Mock(
            status_code=400,
            json=lambda: GoogleMockResponses.TOKEN_EXCHANGE_ERROR,
            raise_for_status=lambda: requests.exceptions.HTTPError()
        )
<<<<<<< HEAD
        
=======

>>>>>>> faace65 (Add comprehensive OAuth security, testing, and coverage infrastructure)
        result = self.provider.exchange_code_for_token(
            code='invalid_code',
            redirect_uri='http://example.com/callback',
            request=self.factory.get('/')
        )
<<<<<<< HEAD
        
        # Should return error information
        self.assertIn('error', result)
        self.assertEqual(result['error'], 'invalid_grant')
    
    def test_service_client_creation(self):
        """Test Google API service client creation."""
        token = OAuthTestData.create_test_token(self.user, provider='google')
        
        with patch.object(self.provider, 'get_valid_token') as mock_get_token:
            mock_get_token.return_value = 'valid_access_token'
            
            client_info = self.provider.get_service_client(token, 'gmail')
            
=======

        # Should return error information
        self.assertIn('error', result)
        self.assertEqual(result['error'], 'invalid_grant')

    def test_service_client_creation(self):
        """Test Google API service client creation."""
        token = OAuthTestData.create_test_token(self.user, provider='google')

        with patch.object(self.provider, 'get_valid_token') as mock_get_token:
            mock_get_token.return_value = 'valid_access_token'

            client_info = self.provider.get_service_client(token, 'gmail')

>>>>>>> faace65 (Add comprehensive OAuth security, testing, and coverage infrastructure)
            self.assertEqual(client_info['service'], 'gmail')
            self.assertEqual(client_info['access_token'], 'valid_access_token')
            self.assertIn('credentials', client_info)
```

### Configuration Example
```python
# Addition to development/development/settings.py

OAUTH2_CONFIG = {
    # ... existing providers ...
    "google": {
        "client_id": os.environ["GOOGLE_CLIENT_ID"],
        "client_secret": os.environ["GOOGLE_CLIENT_SECRET"],
        "scope": " ".join([
            "openid",
<<<<<<< HEAD
            "https://www.googleapis.com/auth/userinfo.email", 
=======
            "https://www.googleapis.com/auth/userinfo.email",
>>>>>>> faace65 (Add comprehensive OAuth security, testing, and coverage infrastructure)
            "https://www.googleapis.com/auth/userinfo.profile",
            # Add additional scopes as needed:
            # "https://www.googleapis.com/auth/gmail.readonly",
            # "https://www.googleapis.com/auth/drive.file",
            # "https://www.googleapis.com/auth/calendar.events",
        ]),
        "include_granted_scopes": "true",  # Incremental authorization
    },
}
```

### Environment Variables
```bash
# development/env.sample
GOOGLE_CLIENT_ID=your_google_client_id_here
GOOGLE_CLIENT_SECRET=your_google_client_secret_here
```

## Success Criteria
- [ ] Complete Google OAuth 2.0 provider implementation
- [ ] Support for standard OAuth flow with offline access
- [ ] Multi-service scope detection and management
- [ ] Comprehensive error handling for Google-specific errors
- [ ] Token validation with Google's tokeninfo endpoint
- [ ] Integration with Google API client libraries (foundation)
- [ ] Complete test coverage including edge cases
- [ ] Documentation for Google Developer Console setup
<<<<<<< HEAD
- [ ] Example usage patterns for different Google services
=======
- [ ] Example usage patterns for different Google services
>>>>>>> faace65 (Add comprehensive OAuth security, testing, and coverage infrastructure)
