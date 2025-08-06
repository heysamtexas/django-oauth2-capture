# Core OAuth Flow Testing Implementation

## Objective
Create comprehensive test coverage for the complete OAuth2 flow including authorization initiation, callback handling, token storage, and refresh cycles. Currently, testing is minimal with only one test for retry logic.

## Context
The OAuth2 flow involves multiple steps that need thorough testing:

1. **Authorization Initiation** (`initiate_oauth2` in views.py:60-84)
<<<<<<< HEAD
2. **Callback Handling** (`oauth2_callback` in views.py:17-57)  
=======
2. **Callback Handling** (`oauth2_callback` in views.py:17-57)
>>>>>>> faace65 (Add comprehensive OAuth security, testing, and coverage infrastructure)
3. **Token Exchange** (provider `exchange_code_for_token` methods)
4. **Token Storage** (`OAuthToken` model operations)
5. **Token Refresh** (`get_valid_token` and `refresh_token` methods)

**Current Testing Gaps:**
- No test coverage for views or OAuth flows
- No mocking of provider APIs
- No integration testing of complete flows
- No testing of Django-specific functionality (sessions, models, etc.)

## Technical Details

### Test Structure
Create comprehensive test suites that cover:
- **Unit Tests**: Individual methods and functions
- **Integration Tests**: Complete OAuth flows end-to-end
- **Mock Tests**: Provider API interactions
- **Django Tests**: Views, models, sessions

### Test Categories
1. **Authorization Flow Tests**: Test initiation and URL generation
2. **Callback Flow Tests**: Test authorization code handling
3. **Token Management Tests**: Test storage, retrieval, updates
4. **Session Management Tests**: Test state handling and cleanup
5. **Model Tests**: Test OAuthToken functionality
6. **Provider Factory Tests**: Test provider instantiation

### Testing Framework Setup
Use Django's built-in testing framework with:
- `TestCase` for database-backed tests
- `RequestFactory` for view testing
- `mock.patch` for external API mocking
- Custom test fixtures for realistic data

## Testing Requirements
<<<<<<< HEAD
1. **Authorization Initiation Tests**: 
=======
1. **Authorization Initiation Tests**:
>>>>>>> faace65 (Add comprehensive OAuth security, testing, and coverage infrastructure)
   - Valid provider authorization URL generation
   - State parameter generation and session storage
   - Invalid provider handling
   - Configuration error scenarios

2. **Callback Handling Tests**:
   - Successful token exchange and storage
   - Invalid authorization codes
   - State verification (from security task)
   - Provider error responses
   - User info retrieval and storage

3. **Token Lifecycle Tests**:
   - Token creation and updates
   - Expiration handling
   - Refresh token functionality
   - Multiple users and providers

4. **Session Management Tests**:
   - State parameter isolation between users
   - Session cleanup after callback
   - Concurrent OAuth flows

## Dependencies
- Mock responses for each provider's API endpoints
- Test data fixtures for realistic scenarios
- May depend on security task implementations (state verification)

## Estimated Complexity
Complex (2-3 days for comprehensive coverage)

## Files to Create
- `oauth2_capture/tests/test_views.py`: View testing
<<<<<<< HEAD
- `oauth2_capture/tests/test_models.py`: Model testing  
=======
- `oauth2_capture/tests/test_models.py`: Model testing
>>>>>>> faace65 (Add comprehensive OAuth security, testing, and coverage infrastructure)
- `oauth2_capture/tests/test_oauth_flows.py`: Integration testing
- `oauth2_capture/tests/fixtures.py`: Test data fixtures
- `oauth2_capture/tests/mocks.py`: Provider API mocks

## Example Code

### Test Base Classes and Fixtures
```python
# oauth2_capture/tests/fixtures.py
from django.contrib.auth.models import User
from oauth2_capture.models import OAuthToken
from datetime import datetime, timedelta
from django.utils import timezone

class OAuthTestData:
    """Test data fixtures for OAuth testing."""
<<<<<<< HEAD
    
=======

>>>>>>> faace65 (Add comprehensive OAuth security, testing, and coverage infrastructure)
    @staticmethod
    def create_test_user(username="testuser"):
        return User.objects.create_user(
            username=username,
            email=f"{username}@example.com",
            password="testpass123"
        )
<<<<<<< HEAD
    
    @staticmethod  
=======

    @staticmethod
>>>>>>> faace65 (Add comprehensive OAuth security, testing, and coverage infrastructure)
    def create_test_token(user, provider="twitter", expired=False):
        expires_at = None
        if not expired:
            expires_at = timezone.now() + timedelta(hours=1)
        else:
            expires_at = timezone.now() - timedelta(hours=1)
<<<<<<< HEAD
            
=======

>>>>>>> faace65 (Add comprehensive OAuth security, testing, and coverage infrastructure)
        return OAuthToken.objects.create(
            provider=provider,
            user_id="12345",
            access_token="test_access_token",
            refresh_token="test_refresh_token",
            expires_at=expires_at,
            token_type="Bearer",
            scope="read write",
            owner=user,
            name="Test User",
            profile_json={"id": "12345", "name": "Test User", "username": "testuser"}
        )
<<<<<<< HEAD
    
=======

>>>>>>> faace65 (Add comprehensive OAuth security, testing, and coverage infrastructure)
    # Mock API responses
    TWITTER_USER_INFO_RESPONSE = {
        "data": {
            "id": "12345",
<<<<<<< HEAD
            "name": "Test User", 
=======
            "name": "Test User",
>>>>>>> faace65 (Add comprehensive OAuth security, testing, and coverage infrastructure)
            "username": "testuser",
            "profile_image_url": "https://example.com/avatar.jpg"
        }
    }
<<<<<<< HEAD
    
    TWITTER_TOKEN_RESPONSE = {
        "access_token": "new_access_token",
        "refresh_token": "new_refresh_token", 
=======

    TWITTER_TOKEN_RESPONSE = {
        "access_token": "new_access_token",
        "refresh_token": "new_refresh_token",
>>>>>>> faace65 (Add comprehensive OAuth security, testing, and coverage infrastructure)
        "expires_in": 3600,
        "token_type": "Bearer",
        "scope": "tweet.read users.read"
    }
<<<<<<< HEAD
    
=======

>>>>>>> faace65 (Add comprehensive OAuth security, testing, and coverage infrastructure)
    GITHUB_USER_INFO_RESPONSE = {
        "id": 67890,
        "login": "testuser",
        "name": "Test User",
        "email": "test@example.com",
        "avatar_url": "https://example.com/avatar.jpg"
    }
```

### Provider API Mocks
```python
# oauth2_capture/tests/mocks.py
import json
from unittest.mock import Mock
import requests

class MockProviderAPI:
    """Mock provider API responses for testing."""
<<<<<<< HEAD
    
    def __init__(self, provider_name):
        self.provider_name = provider_name
        self.responses = {}
        
=======

    def __init__(self, provider_name):
        self.provider_name = provider_name
        self.responses = {}

>>>>>>> faace65 (Add comprehensive OAuth security, testing, and coverage infrastructure)
    def mock_token_exchange(self, success=True, token_data=None):
        """Mock token exchange endpoint."""
        if success:
            response_data = token_data or OAuthTestData.TWITTER_TOKEN_RESPONSE
        else:
            response_data = {"error": "invalid_grant", "error_description": "Invalid authorization code"}
<<<<<<< HEAD
            
=======

>>>>>>> faace65 (Add comprehensive OAuth security, testing, and coverage infrastructure)
        mock_response = Mock(spec=requests.Response)
        mock_response.status_code = 200 if success else 400
        mock_response.json.return_value = response_data
        mock_response.text = json.dumps(response_data)
<<<<<<< HEAD
        
        return mock_response
    
=======

        return mock_response

>>>>>>> faace65 (Add comprehensive OAuth security, testing, and coverage infrastructure)
    def mock_user_info(self, success=True, user_data=None):
        """Mock user info endpoint."""
        if success:
            response_data = user_data or OAuthTestData.TWITTER_USER_INFO_RESPONSE
        else:
            response_data = {"error": "invalid_token"}
<<<<<<< HEAD
            
        mock_response = Mock(spec=requests.Response) 
        mock_response.status_code = 200 if success else 401
        mock_response.json.return_value = response_data
        mock_response.text = json.dumps(response_data)
        
        return mock_response
    
=======

        mock_response = Mock(spec=requests.Response)
        mock_response.status_code = 200 if success else 401
        mock_response.json.return_value = response_data
        mock_response.text = json.dumps(response_data)

        return mock_response

>>>>>>> faace65 (Add comprehensive OAuth security, testing, and coverage infrastructure)
    def mock_token_refresh(self, success=True, token_data=None):
        """Mock token refresh endpoint."""
        if success:
            response_data = token_data or {
                "access_token": "refreshed_access_token",
                "expires_in": 3600,
                "token_type": "Bearer"
            }
        else:
            response_data = {"error": "invalid_grant", "error_description": "Refresh token expired"}
<<<<<<< HEAD
            
=======

>>>>>>> faace65 (Add comprehensive OAuth security, testing, and coverage infrastructure)
        mock_response = Mock(spec=requests.Response)
        mock_response.status_code = 200 if success else 400
        mock_response.json.return_value = response_data
        mock_response.text = json.dumps(response_data)
<<<<<<< HEAD
        
=======

>>>>>>> faace65 (Add comprehensive OAuth security, testing, and coverage infrastructure)
        return mock_response
```

### View Testing
```python
# oauth2_capture/tests/test_views.py
from django.test import TestCase, RequestFactory
from django.contrib.auth.models import User
<<<<<<< HEAD
from django.contrib.sessions.middleware import SessionMiddleware  
=======
from django.contrib.sessions.middleware import SessionMiddleware
>>>>>>> faace65 (Add comprehensive OAuth security, testing, and coverage infrastructure)
from unittest.mock import patch, Mock
from oauth2_capture.views import initiate_oauth2, oauth2_callback
from oauth2_capture.models import OAuthToken
from .fixtures import OAuthTestData
from .mocks import MockProviderAPI

class OAuth2ViewTests(TestCase):
<<<<<<< HEAD
    
=======

>>>>>>> faace65 (Add comprehensive OAuth security, testing, and coverage infrastructure)
    def setUp(self):
        self.factory = RequestFactory()
        self.user = OAuthTestData.create_test_user()
        self.mock_api = MockProviderAPI('twitter')
<<<<<<< HEAD
    
=======

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
    def test_initiate_oauth2_valid_provider(self):
        """Test OAuth initiation with valid provider."""
        request = self.factory.get('/oauth2/twitter/authorize/')
        request.user = self.user
        request = self.add_session_to_request(request)
<<<<<<< HEAD
        
        response = initiate_oauth2(request, 'twitter')
        
        # Should redirect to provider authorization URL
        self.assertEqual(response.status_code, 302)
        self.assertIn('twitter.com', response.url)
        
=======

        response = initiate_oauth2(request, 'twitter')

        # Should redirect to provider authorization URL
        self.assertEqual(response.status_code, 302)
        self.assertIn('twitter.com', response.url)

>>>>>>> faace65 (Add comprehensive OAuth security, testing, and coverage infrastructure)
        # Should store state in session
        self.assertIn('twitter_oauth_state', request.session)
        state = request.session['twitter_oauth_state']
        self.assertEqual(len(state), 43)  # URL-safe base64 32 bytes
<<<<<<< HEAD
    
=======

>>>>>>> faace65 (Add comprehensive OAuth security, testing, and coverage infrastructure)
    def test_initiate_oauth2_invalid_provider(self):
        """Test OAuth initiation with unsupported provider."""
        request = self.factory.get('/oauth2/invalid/authorize/')
        request.user = self.user
        request = self.add_session_to_request(request)
<<<<<<< HEAD
        
        response = initiate_oauth2(request, 'invalid')
        
        self.assertEqual(response.status_code, 400)
        self.assertIn('Unsupported provider', response.content.decode())
    
=======

        response = initiate_oauth2(request, 'invalid')

        self.assertEqual(response.status_code, 400)
        self.assertIn('Unsupported provider', response.content.decode())

>>>>>>> faace65 (Add comprehensive OAuth security, testing, and coverage infrastructure)
    @patch('requests.post')
    @patch('requests.get')
    def test_oauth2_callback_success(self, mock_get, mock_post):
        """Test successful OAuth callback flow."""
        # Setup mocks
        mock_post.return_value = self.mock_api.mock_token_exchange(success=True)
        mock_get.return_value = self.mock_api.mock_user_info(success=True)
<<<<<<< HEAD
        
=======

>>>>>>> faace65 (Add comprehensive OAuth security, testing, and coverage infrastructure)
        # Setup request with session state
        request = self.factory.get('/oauth2/twitter/callback/?code=test_code&state=test_state')
        request.user = self.user
        request = self.add_session_to_request(request)
        request.session['twitter_oauth_state'] = 'test_state'
<<<<<<< HEAD
        
        response = oauth2_callback(request, 'twitter')
        
        # Should succeed
        self.assertEqual(response.status_code, 200)
        self.assertIn('connected successfully', response.content.decode())
        
=======

        response = oauth2_callback(request, 'twitter')

        # Should succeed
        self.assertEqual(response.status_code, 200)
        self.assertIn('connected successfully', response.content.decode())

>>>>>>> faace65 (Add comprehensive OAuth security, testing, and coverage infrastructure)
        # Should create token
        token = OAuthToken.objects.filter(provider='twitter', owner=self.user).first()
        self.assertIsNotNone(token)
        self.assertEqual(token.access_token, 'new_access_token')
        self.assertEqual(token.user_id, '12345')
<<<<<<< HEAD
        
        # Should clear session state
        self.assertNotIn('twitter_oauth_state', request.session)
    
=======

        # Should clear session state
        self.assertNotIn('twitter_oauth_state', request.session)

>>>>>>> faace65 (Add comprehensive OAuth security, testing, and coverage infrastructure)
    def test_oauth2_callback_invalid_state(self):
        """Test callback with invalid state parameter."""
        request = self.factory.get('/oauth2/twitter/callback/?code=test_code&state=wrong_state')
        request.user = self.user
        request = self.add_session_to_request(request)
        request.session['twitter_oauth_state'] = 'correct_state'
<<<<<<< HEAD
        
        response = oauth2_callback(request, 'twitter')
        
        self.assertEqual(response.status_code, 400)
        self.assertIn('state', response.content.decode().lower())
    
=======

        response = oauth2_callback(request, 'twitter')

        self.assertEqual(response.status_code, 400)
        self.assertIn('state', response.content.decode().lower())

>>>>>>> faace65 (Add comprehensive OAuth security, testing, and coverage infrastructure)
    def test_oauth2_callback_missing_code(self):
        """Test callback without authorization code."""
        request = self.factory.get('/oauth2/twitter/callback/?state=test_state')
        request.user = self.user
        request = self.add_session_to_request(request)
        request.session['twitter_oauth_state'] = 'test_state'
<<<<<<< HEAD
        
        response = oauth2_callback(request, 'twitter')
        
        self.assertEqual(response.status_code, 400)
        self.assertIn('code', response.content.decode().lower())
    
=======

        response = oauth2_callback(request, 'twitter')

        self.assertEqual(response.status_code, 400)
        self.assertIn('code', response.content.decode().lower())

>>>>>>> faace65 (Add comprehensive OAuth security, testing, and coverage infrastructure)
    @patch('requests.post')
    def test_oauth2_callback_token_exchange_failure(self, mock_post):
        """Test callback when token exchange fails."""
        mock_post.return_value = self.mock_api.mock_token_exchange(success=False)
<<<<<<< HEAD
        
=======

>>>>>>> faace65 (Add comprehensive OAuth security, testing, and coverage infrastructure)
        request = self.factory.get('/oauth2/twitter/callback/?code=test_code&state=test_state')
        request.user = self.user
        request = self.add_session_to_request(request)
        request.session['twitter_oauth_state'] = 'test_state'
<<<<<<< HEAD
        
        response = oauth2_callback(request, 'twitter')
        
=======

        response = oauth2_callback(request, 'twitter')

>>>>>>> faace65 (Add comprehensive OAuth security, testing, and coverage infrastructure)
        self.assertEqual(response.status_code, 400)
        self.assertIn('Failed to connect', response.content.decode())
```

### Integration Testing
```python
# oauth2_capture/tests/test_oauth_flows.py
from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from unittest.mock import patch
from oauth2_capture.models import OAuthToken
from .fixtures import OAuthTestData
from .mocks import MockProviderAPI

class OAuth2IntegrationTests(TestCase):
<<<<<<< HEAD
    
=======

>>>>>>> faace65 (Add comprehensive OAuth security, testing, and coverage infrastructure)
    def setUp(self):
        self.client = Client()
        self.user = OAuthTestData.create_test_user()
        self.client.force_login(self.user)
        self.mock_api = MockProviderAPI('twitter')
<<<<<<< HEAD
    
    @patch('requests.post')
    @patch('requests.get') 
    def test_complete_oauth_flow(self, mock_get, mock_post):
        """Test complete OAuth flow from start to finish."""
        
        # Step 1: Initiate OAuth
        response = self.client.get(reverse('oauth2_capture:authorize', args=['twitter']))
        
        self.assertEqual(response.status_code, 302)
        self.assertIn('twitter.com', response.url)
        
=======

    @patch('requests.post')
    @patch('requests.get')
    def test_complete_oauth_flow(self, mock_get, mock_post):
        """Test complete OAuth flow from start to finish."""

        # Step 1: Initiate OAuth
        response = self.client.get(reverse('oauth2_capture:authorize', args=['twitter']))

        self.assertEqual(response.status_code, 302)
        self.assertIn('twitter.com', response.url)

>>>>>>> faace65 (Add comprehensive OAuth security, testing, and coverage infrastructure)
        # Extract state from session
        session = self.client.session
        state = session['twitter_oauth_state']
        self.assertTrue(state)
<<<<<<< HEAD
        
        # Step 2: Simulate provider callback
        mock_post.return_value = self.mock_api.mock_token_exchange(success=True)
        mock_get.return_value = self.mock_api.mock_user_info(success=True)
        
        callback_url = reverse('oauth2_capture:callback', args=['twitter'])
        response = self.client.get(f'{callback_url}?code=test_code&state={state}')
        
        self.assertEqual(response.status_code, 200)
        self.assertIn('connected successfully', response.content.decode())
        
=======

        # Step 2: Simulate provider callback
        mock_post.return_value = self.mock_api.mock_token_exchange(success=True)
        mock_get.return_value = self.mock_api.mock_user_info(success=True)

        callback_url = reverse('oauth2_capture:callback', args=['twitter'])
        response = self.client.get(f'{callback_url}?code=test_code&state={state}')

        self.assertEqual(response.status_code, 200)
        self.assertIn('connected successfully', response.content.decode())

>>>>>>> faace65 (Add comprehensive OAuth security, testing, and coverage infrastructure)
        # Step 3: Verify token was created
        token = OAuthToken.objects.filter(provider='twitter', owner=self.user).first()
        self.assertIsNotNone(token)
        self.assertEqual(token.access_token, 'new_access_token')
        self.assertEqual(token.refresh_token, 'new_refresh_token')
<<<<<<< HEAD
        
        # Step 4: Test token refresh
        token.expires_at = timezone.now() - timedelta(minutes=1)  # Make expired
        token.save()
        
        mock_post.return_value = self.mock_api.mock_token_refresh(success=True)
        
        provider = OAuth2ProviderFactory.get_provider('twitter')
        refreshed_token = provider.get_valid_token(token)
        
        self.assertEqual(refreshed_token, 'refreshed_access_token')
        
        # Reload token to check updates
        token.refresh_from_db()
        self.assertEqual(token.access_token, 'refreshed_access_token')
    
    def test_multiple_user_isolation(self):
        """Test that OAuth flows are isolated between users."""
        user2 = OAuthTestData.create_test_user(username="user2")
        
        # User 1 starts OAuth flow
        response1 = self.client.get(reverse('oauth2_capture:authorize', args=['twitter']))
        state1 = self.client.session['twitter_oauth_state']
        
        # User 2 starts OAuth flow  
        self.client.force_login(user2)
        response2 = self.client.get(reverse('oauth2_capture:authorize', args=['twitter']))
        state2 = self.client.session['twitter_oauth_state']
        
        # States should be different
        self.assertNotEqual(state1, state2)
        
        # User 2's callback shouldn't work with User 1's state
        callback_url = reverse('oauth2_capture:callback', args=['twitter'])
        response = self.client.get(f'{callback_url}?code=test_code&state={state1}')
        
=======

        # Step 4: Test token refresh
        token.expires_at = timezone.now() - timedelta(minutes=1)  # Make expired
        token.save()

        mock_post.return_value = self.mock_api.mock_token_refresh(success=True)

        provider = OAuth2ProviderFactory.get_provider('twitter')
        refreshed_token = provider.get_valid_token(token)

        self.assertEqual(refreshed_token, 'refreshed_access_token')

        # Reload token to check updates
        token.refresh_from_db()
        self.assertEqual(token.access_token, 'refreshed_access_token')

    def test_multiple_user_isolation(self):
        """Test that OAuth flows are isolated between users."""
        user2 = OAuthTestData.create_test_user(username="user2")

        # User 1 starts OAuth flow
        response1 = self.client.get(reverse('oauth2_capture:authorize', args=['twitter']))
        state1 = self.client.session['twitter_oauth_state']

        # User 2 starts OAuth flow
        self.client.force_login(user2)
        response2 = self.client.get(reverse('oauth2_capture:authorize', args=['twitter']))
        state2 = self.client.session['twitter_oauth_state']

        # States should be different
        self.assertNotEqual(state1, state2)

        # User 2's callback shouldn't work with User 1's state
        callback_url = reverse('oauth2_capture:callback', args=['twitter'])
        response = self.client.get(f'{callback_url}?code=test_code&state={state1}')

>>>>>>> faace65 (Add comprehensive OAuth security, testing, and coverage infrastructure)
        self.assertEqual(response.status_code, 400)  # State mismatch
```

### Model Testing
```python
# oauth2_capture/tests/test_models.py
from django.test import TestCase
from django.utils import timezone
from datetime import timedelta
from oauth2_capture.models import OAuthToken
from .fixtures import OAuthTestData

class OAuthTokenModelTests(TestCase):
<<<<<<< HEAD
    
    def setUp(self):
        self.user = OAuthTestData.create_test_user()
    
=======

    def setUp(self):
        self.user = OAuthTestData.create_test_user()

>>>>>>> faace65 (Add comprehensive OAuth security, testing, and coverage infrastructure)
    def test_token_expiration_check(self):
        """Test token expiration property."""
        # Non-expired token
        token = OAuthTestData.create_test_token(self.user, expired=False)
        self.assertFalse(token.is_expired)
<<<<<<< HEAD
        
        # Expired token
        expired_token = OAuthTestData.create_test_token(self.user, expired=True)
        self.assertTrue(expired_token.is_expired)
        
=======

        # Expired token
        expired_token = OAuthTestData.create_test_token(self.user, expired=True)
        self.assertTrue(expired_token.is_expired)

>>>>>>> faace65 (Add comprehensive OAuth security, testing, and coverage infrastructure)
        # Token with no expiration
        token.expires_at = None
        token.save()
        self.assertFalse(token.is_expired)
<<<<<<< HEAD
    
=======

>>>>>>> faace65 (Add comprehensive OAuth security, testing, and coverage infrastructure)
    def test_token_string_representation(self):
        """Test model string representation."""
        token = OAuthTestData.create_test_token(self.user)
        expected = f"twitter (Test User) @ {self.user}"
        self.assertEqual(str(token), expected)
<<<<<<< HEAD
    
=======

>>>>>>> faace65 (Add comprehensive OAuth security, testing, and coverage infrastructure)
    def test_unique_constraint(self):
        """Test unique constraint on provider + user_id."""
        # Create first token
        OAuthTestData.create_test_token(self.user)
<<<<<<< HEAD
        
        # Creating second token with same provider + user_id should fail
        with self.assertRaises(IntegrityError):
            OAuthTestData.create_test_token(self.user)
    
    def test_username_property(self):
        """Test username property extraction from profile_json."""
        token = OAuthTestData.create_test_token(self.user)
        
        # Should use 'username' from profile_json
        self.assertEqual(token.username, "testuser")
        
        # Test fallback to 'login' 
        token.profile_json = {"id": "12345", "login": "github_user"}
        token.save()
        self.assertEqual(token.username, "github_user")
        
=======

        # Creating second token with same provider + user_id should fail
        with self.assertRaises(IntegrityError):
            OAuthTestData.create_test_token(self.user)

    def test_username_property(self):
        """Test username property extraction from profile_json."""
        token = OAuthTestData.create_test_token(self.user)

        # Should use 'username' from profile_json
        self.assertEqual(token.username, "testuser")

        # Test fallback to 'login'
        token.profile_json = {"id": "12345", "login": "github_user"}
        token.save()
        self.assertEqual(token.username, "github_user")

>>>>>>> faace65 (Add comprehensive OAuth security, testing, and coverage infrastructure)
        # Test fallback to name field
        token.profile_json = {"id": "12345"}
        token.save()
        self.assertEqual(token.username, "Test User")
```

## Success Criteria
- [ ] Complete test coverage for all OAuth flow components
- [ ] Mocked external API calls for reliable testing
- [ ] Integration tests covering end-to-end flows
- [ ] Edge case testing for error scenarios
- [ ] Performance testing for concurrent flows
- [ ] Test isolation and cleanup
- [ ] Comprehensive assertion coverage
<<<<<<< HEAD
- [ ] Documentation of test scenarios and expected behaviors
=======
- [ ] Documentation of test scenarios and expected behaviors
>>>>>>> faace65 (Add comprehensive OAuth security, testing, and coverage infrastructure)
