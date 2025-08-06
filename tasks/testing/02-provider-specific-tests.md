# Provider-Specific OAuth Testing

## Objective
Create comprehensive test coverage for each OAuth provider's specific implementation details, quirks, and edge cases. Each provider has unique characteristics that need individual testing beyond the generic OAuth flow tests.

## Context
Each provider implementation in `oauth2_capture/services/oauth2.py` has provider-specific behavior:

**Twitter (lines 273-371):**
- PKCE implementation with code verifier/challenge
- Session-based code verifier storage
- Bearer token authentication
- Specific user info API structure

**LinkedIn (lines 373-437):**
- Standard OAuth2 flow
- Userinfo endpoint with sub claim mapping
- Form-encoded token exchange

**GitHub (lines 440-507):**
- Token prefix "token" instead of "Bearer"
- Null name handling in user info
- Simple POST token exchange

**Reddit (lines 509-607):**
- HTTP Basic Auth requirement
- Custom User-Agent header requirement
- Permanent duration parameter
- Special refresh token handling

**Pinterest (lines 637-710):**
- HTTP Basic Auth for token exchange
- Username to ID mapping
- Name field handling

**Facebook (lines 712-779):**
- GET request for token exchange
- Picture data structure handling
- Profile image URL extraction

## Technical Details

### Test Coverage Per Provider
1. **Authorization URL Generation**: Provider-specific parameters and endpoints
2. **Token Exchange**: Provider-specific authentication methods and data formats
3. **User Info Retrieval**: Provider-specific API structures and field mappings
4. **Token Refresh**: Provider-specific refresh implementations
5. **Error Handling**: Provider-specific error responses and codes
6. **Edge Cases**: Provider-specific quirks and workarounds

### Mock Strategy
Each provider needs realistic API response mocks based on their actual API documentation and response formats.

## Testing Requirements
1. **Authorization Tests**: Verify correct authorization URLs with provider-specific parameters
2. **Token Exchange Tests**: Test provider-specific authentication and request formats
3. **User Info Tests**: Verify correct parsing of provider-specific user data
4. **Refresh Token Tests**: Test provider-specific refresh implementations
5. **Error Response Tests**: Test handling of provider-specific error formats
6. **Edge Case Tests**: Test provider-specific quirks and workarounds

## Dependencies
- Realistic API response mocks for each provider
- Provider API documentation for accurate testing
- Core OAuth flow tests (from task 01) as foundation

## Estimated Complexity
Medium (1 day per provider, can be done in parallel)

## Files to Create
- `oauth2_capture/tests/providers/test_twitter.py`: Twitter-specific tests
- `oauth2_capture/tests/providers/test_linkedin.py`: LinkedIn-specific tests
- `oauth2_capture/tests/providers/test_github.py`: GitHub-specific tests
- `oauth2_capture/tests/providers/test_reddit.py`: Reddit-specific tests
- `oauth2_capture/tests/providers/test_pinterest.py`: Pinterest-specific tests
- `oauth2_capture/tests/providers/test_facebook.py`: Facebook-specific tests
- `oauth2_capture/tests/providers/__init__.py`: Provider test utilities
- `oauth2_capture/tests/providers/mock_responses.py`: Realistic API response data

## Example Code

### Provider Mock Responses
```python
# oauth2_capture/tests/providers/mock_responses.py
"""Realistic API response mocks based on actual provider APIs."""

class TwitterMockResponses:
    """Twitter API v2 response mocks."""
<<<<<<< HEAD
    
=======

>>>>>>> faace65 (Add comprehensive OAuth security, testing, and coverage infrastructure)
    TOKEN_EXCHANGE_SUCCESS = {
        "access_token": "VGhpcyBpcyBhbiCDIGFjY2VzcyB0b2tlbg",
        "refresh_token": "bWV0aW1ldCB0aGlzIGNvdWxkIGJlIGEgcmVmcmVzaCB0b2tlbg",
        "expires_in": 7200,
        "scope": "tweet.read users.read tweet.write offline.access",
        "token_type": "bearer"
    }
<<<<<<< HEAD
    
    TOKEN_REFRESH_SUCCESS = {
        "access_token": "bmV3IGFjY2VzcyB0b2tlbiBmcm9tIHJlZnJlc2g",
        "refresh_token": "bmV3IHJlZnJlc2ggdG9rZW4gZnJvbSByZWZyZXNo", 
=======

    TOKEN_REFRESH_SUCCESS = {
        "access_token": "bmV3IGFjY2VzcyB0b2tlbiBmcm9tIHJlZnJlc2g",
        "refresh_token": "bmV3IHJlZnJlc2ggdG9rZW4gZnJvbSByZWZyZXNo",
>>>>>>> faace65 (Add comprehensive OAuth security, testing, and coverage infrastructure)
        "expires_in": 7200,
        "scope": "tweet.read users.read tweet.write offline.access",
        "token_type": "bearer"
    }
<<<<<<< HEAD
    
=======

>>>>>>> faace65 (Add comprehensive OAuth security, testing, and coverage infrastructure)
    USER_INFO_SUCCESS = {
        "data": {
            "id": "2244994945",
            "name": "Twitter Dev",
            "username": "TwitterDev",
            "profile_image_url": "https://pbs.twimg.com/profile_images/1283786620521652229/lEODkLTh_normal.jpg",
            "description": "The voice of the Twitter developer community."
        }
    }
<<<<<<< HEAD
    
=======

>>>>>>> faace65 (Add comprehensive OAuth security, testing, and coverage infrastructure)
    TOKEN_EXCHANGE_ERROR = {
        "error": "invalid_grant",
        "error_description": "Value passed for the authorization code was invalid."
    }

class LinkedInMockResponses:
    """LinkedIn API response mocks."""
<<<<<<< HEAD
    
=======

>>>>>>> faace65 (Add comprehensive OAuth security, testing, and coverage infrastructure)
    TOKEN_EXCHANGE_SUCCESS = {
        "access_token": "AQXdSP_W41_UPs5ioT_t8HESyODB4FqbWw",
        "expires_in": 5184000,
        "scope": "profile,email,openid,w_member_social",
        "token_type": "Bearer"
    }
<<<<<<< HEAD
    
    USER_INFO_SUCCESS = {
        "sub": "xyz123abc",
        "name": "Jane Doe", 
=======

    USER_INFO_SUCCESS = {
        "sub": "xyz123abc",
        "name": "Jane Doe",
>>>>>>> faace65 (Add comprehensive OAuth security, testing, and coverage infrastructure)
        "given_name": "Jane",
        "family_name": "Doe",
        "picture": "https://media.licdn.com/media/profile-image.jpg",
        "email": "jane.doe@example.com",
        "email_verified": True,
        "locale": "en-US"
    }

class GitHubMockResponses:
    """GitHub API response mocks."""
<<<<<<< HEAD
    
=======

>>>>>>> faace65 (Add comprehensive OAuth security, testing, and coverage infrastructure)
    TOKEN_EXCHANGE_SUCCESS = {
        "access_token": "gho_16C7e42F292c6912E7710c838347Ae178B4a",
        "token_type": "bearer",
        "scope": "user,repo"
    }
<<<<<<< HEAD
    
=======

>>>>>>> faace65 (Add comprehensive OAuth security, testing, and coverage infrastructure)
    USER_INFO_SUCCESS = {
        "login": "octocat",
        "id": 1,
        "node_id": "MDQ6VXNlcjE=",
        "avatar_url": "https://github.com/images/error/octocat_happy.gif",
        "gravatar_id": "",
        "name": "The Octocat",
        "company": "GitHub",
        "blog": "https://github.com/blog",
        "location": "San Francisco",
        "email": "octocat@github.com",
        "hireable": False,
        "bio": "There once was...",
        "twitter_username": "octocat",
        "public_repos": 2,
        "public_gists": 1,
        "followers": 20,
        "following": 0,
        "created_at": "2008-01-14T04:33:35Z",
        "updated_at": "2008-01-14T04:33:35Z"
    }
<<<<<<< HEAD
    
=======

>>>>>>> faace65 (Add comprehensive OAuth security, testing, and coverage infrastructure)
    # Test null name handling
    USER_INFO_NULL_NAME = {
        "login": "testuser",
        "id": 12345,
        "name": None,  # This is what GitHub returns sometimes
        "email": "test@example.com"
    }

class RedditMockResponses:
    """Reddit API response mocks."""
<<<<<<< HEAD
    
    TOKEN_EXCHANGE_SUCCESS = {
        "access_token": "abc123def456",
        "token_type": "bearer", 
=======

    TOKEN_EXCHANGE_SUCCESS = {
        "access_token": "abc123def456",
        "token_type": "bearer",
>>>>>>> faace65 (Add comprehensive OAuth security, testing, and coverage infrastructure)
        "expires_in": 3600,
        "scope": "identity edit read submit save",
        "refresh_token": "xyz789uvw012"
    }
<<<<<<< HEAD
    
=======

>>>>>>> faace65 (Add comprehensive OAuth security, testing, and coverage infrastructure)
    USER_INFO_SUCCESS = {
        "kind": "t2",
        "data": {
            "id": "2fwo",
            "name": "testuser",
            "created": 1234567890.0,
            "link_karma": 100,
            "comment_karma": 200,
            "is_gold": False,
            "has_verified_email": True
        }
    }
<<<<<<< HEAD
    
=======

>>>>>>> faace65 (Add comprehensive OAuth security, testing, and coverage infrastructure)
    TOKEN_EXCHANGE_ERROR = {
        "error": "invalid_grant"
    }
```

### Twitter-Specific Tests
```python
# oauth2_capture/tests/providers/test_twitter.py
from django.test import TestCase, RequestFactory
from django.contrib.sessions.middleware import SessionMiddleware
from unittest.mock import patch, Mock
import json

from oauth2_capture.services.oauth2 import TwitterOAuth2Provider
from oauth2_capture.models import OAuthToken
from ..fixtures import OAuthTestData
from .mock_responses import TwitterMockResponses

class TwitterProviderTests(TestCase):
<<<<<<< HEAD
    
=======

>>>>>>> faace65 (Add comprehensive OAuth security, testing, and coverage infrastructure)
    def setUp(self):
        self.provider = TwitterOAuth2Provider('twitter')
        self.factory = RequestFactory()
        self.user = OAuthTestData.create_test_user()
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
    def test_authorization_url_includes_pkce(self):
        """Test that Twitter authorization URL includes PKCE parameters."""
        request = self.factory.get('/')
        request = self.add_session_to_request(request)
<<<<<<< HEAD
        
=======

>>>>>>> faace65 (Add comprehensive OAuth security, testing, and coverage infrastructure)
        auth_url = self.provider.get_authorization_url(
            state='test_state',
            redirect_uri='http://example.com/callback',
            request=request
        )
<<<<<<< HEAD
        
        # Should include PKCE parameters
        self.assertIn('code_challenge=', auth_url)
        self.assertIn('code_challenge_method=S256', auth_url)
        
        # Should store code verifier in session
        self.assertIn('code_verifier', request.session)
        
        # Code verifier should be URL-safe base64
        code_verifier = request.session['code_verifier']
        self.assertTrue(len(code_verifier) > 120)  # Should be at least 128 chars when encoded
        
=======

        # Should include PKCE parameters
        self.assertIn('code_challenge=', auth_url)
        self.assertIn('code_challenge_method=S256', auth_url)

        # Should store code verifier in session
        self.assertIn('code_verifier', request.session)

        # Code verifier should be URL-safe base64
        code_verifier = request.session['code_verifier']
        self.assertTrue(len(code_verifier) > 120)  # Should be at least 128 chars when encoded

>>>>>>> faace65 (Add comprehensive OAuth security, testing, and coverage infrastructure)
    def test_authorization_url_parameters(self):
        """Test Twitter authorization URL contains correct parameters."""
        request = self.factory.get('/')
        request = self.add_session_to_request(request)
<<<<<<< HEAD
        
        auth_url = self.provider.get_authorization_url(
            state='test_state',
            redirect_uri='http://example.com/callback', 
            request=request
        )
        
        # Check base URL
        self.assertIn('https://twitter.com/i/oauth2/authorize', auth_url)
        
=======

        auth_url = self.provider.get_authorization_url(
            state='test_state',
            redirect_uri='http://example.com/callback',
            request=request
        )

        # Check base URL
        self.assertIn('https://twitter.com/i/oauth2/authorize', auth_url)

>>>>>>> faace65 (Add comprehensive OAuth security, testing, and coverage infrastructure)
        # Check required parameters
        self.assertIn('client_id=', auth_url)
        self.assertIn('redirect_uri=', auth_url)
        self.assertIn('response_type=code', auth_url)
        self.assertIn('state=test_state', auth_url)
        self.assertIn('scope=', auth_url)
<<<<<<< HEAD
        
=======

>>>>>>> faace65 (Add comprehensive OAuth security, testing, and coverage infrastructure)
    @patch('requests.post')
    def test_token_exchange_with_pkce(self, mock_post):
        """Test Twitter token exchange includes PKCE code verifier."""
        mock_post.return_value = Mock(
            json=lambda: TwitterMockResponses.TOKEN_EXCHANGE_SUCCESS,
            status_code=200
        )
<<<<<<< HEAD
        
        request = self.factory.get('/')
        request = self.add_session_to_request(request)
        request.session['code_verifier'] = 'test_code_verifier'
        
=======

        request = self.factory.get('/')
        request = self.add_session_to_request(request)
        request.session['code_verifier'] = 'test_code_verifier'

>>>>>>> faace65 (Add comprehensive OAuth security, testing, and coverage infrastructure)
        result = self.provider.exchange_code_for_token(
            code='test_code',
            redirect_uri='http://example.com/callback',
            request=request
        )
<<<<<<< HEAD
        
        # Should call token endpoint with PKCE
        mock_post.assert_called_once()
        call_args = mock_post.call_args
        
        # Check data includes code_verifier
        self.assertIn('code_verifier', call_args[1]['data'])
        self.assertEqual(call_args[1]['data']['code_verifier'], 'test_code_verifier')
        
        # Check Basic Auth header
        self.assertIn('Authorization', call_args[1]['headers'])
        self.assertIn('Basic ', call_args[1]['headers']['Authorization'])
        
        # Check response parsing
        self.assertEqual(result['access_token'], TwitterMockResponses.TOKEN_EXCHANGE_SUCCESS['access_token'])
        
=======

        # Should call token endpoint with PKCE
        mock_post.assert_called_once()
        call_args = mock_post.call_args

        # Check data includes code_verifier
        self.assertIn('code_verifier', call_args[1]['data'])
        self.assertEqual(call_args[1]['data']['code_verifier'], 'test_code_verifier')

        # Check Basic Auth header
        self.assertIn('Authorization', call_args[1]['headers'])
        self.assertIn('Basic ', call_args[1]['headers']['Authorization'])

        # Check response parsing
        self.assertEqual(result['access_token'], TwitterMockResponses.TOKEN_EXCHANGE_SUCCESS['access_token'])

>>>>>>> faace65 (Add comprehensive OAuth security, testing, and coverage infrastructure)
    @patch('requests.get')
    def test_user_info_parsing(self, mock_get):
        """Test Twitter user info parsing and field extraction."""
        mock_get.return_value = Mock(
            json=lambda: TwitterMockResponses.USER_INFO_SUCCESS,
            status_code=200
        )
<<<<<<< HEAD
        
        result = self.provider.get_user_info('test_token')
        
        # Should extract data from nested structure
        expected_data = TwitterMockResponses.USER_INFO_SUCCESS['data']
        self.assertEqual(result, expected_data)
        
        # Check API call parameters
        mock_get.assert_called_once()
        call_args = mock_get.call_args
        
        # Should use Bearer token
        self.assertEqual(call_args[1]['headers']['Authorization'], 'Bearer test_token')
        
        # Should request minimal fields
        self.assertIn('user.fields', call_args[1]['params'])
        
=======

        result = self.provider.get_user_info('test_token')

        # Should extract data from nested structure
        expected_data = TwitterMockResponses.USER_INFO_SUCCESS['data']
        self.assertEqual(result, expected_data)

        # Check API call parameters
        mock_get.assert_called_once()
        call_args = mock_get.call_args

        # Should use Bearer token
        self.assertEqual(call_args[1]['headers']['Authorization'], 'Bearer test_token')

        # Should request minimal fields
        self.assertIn('user.fields', call_args[1]['params'])

>>>>>>> faace65 (Add comprehensive OAuth security, testing, and coverage infrastructure)
    @patch('requests.post')
    def test_token_refresh(self, mock_post):
        """Test Twitter token refresh with Basic Auth."""
        mock_post.return_value = Mock(
            json=lambda: TwitterMockResponses.TOKEN_REFRESH_SUCCESS,
            status_code=200
        )
<<<<<<< HEAD
        
        result = self.provider.refresh_token('test_refresh_token')
        
        # Should call with Basic Auth
        mock_post.assert_called_once()
        call_args = mock_post.call_args
        
        self.assertIn('Authorization', call_args[1]['headers'])
        self.assertIn('Basic ', call_args[1]['headers']['Authorization'])
        
        # Should include refresh token
        self.assertIn('refresh_token', call_args[1]['data'])
        self.assertEqual(call_args[1]['data']['refresh_token'], 'test_refresh_token')
        
        # Should parse response correctly
        self.assertEqual(result['access_token'], TwitterMockResponses.TOKEN_REFRESH_SUCCESS['access_token'])
        
=======

        result = self.provider.refresh_token('test_refresh_token')

        # Should call with Basic Auth
        mock_post.assert_called_once()
        call_args = mock_post.call_args

        self.assertIn('Authorization', call_args[1]['headers'])
        self.assertIn('Basic ', call_args[1]['headers']['Authorization'])

        # Should include refresh token
        self.assertIn('refresh_token', call_args[1]['data'])
        self.assertEqual(call_args[1]['data']['refresh_token'], 'test_refresh_token')

        # Should parse response correctly
        self.assertEqual(result['access_token'], TwitterMockResponses.TOKEN_REFRESH_SUCCESS['access_token'])

>>>>>>> faace65 (Add comprehensive OAuth security, testing, and coverage infrastructure)
    @patch('requests.post')
    def test_token_exchange_error_handling(self, mock_post):
        """Test Twitter token exchange error response handling."""
        mock_post.return_value = Mock(
            json=lambda: TwitterMockResponses.TOKEN_EXCHANGE_ERROR,
            status_code=400,
            text=json.dumps(TwitterMockResponses.TOKEN_EXCHANGE_ERROR)
        )
<<<<<<< HEAD
        
        request = self.factory.get('/')
        request = self.add_session_to_request(request)
        request.session['code_verifier'] = 'test_code_verifier'
        
=======

        request = self.factory.get('/')
        request = self.add_session_to_request(request)
        request.session['code_verifier'] = 'test_code_verifier'

>>>>>>> faace65 (Add comprehensive OAuth security, testing, and coverage infrastructure)
        result = self.provider.exchange_code_for_token(
            code='invalid_code',
            redirect_uri='http://example.com/callback',
            request=request
        )
<<<<<<< HEAD
        
=======

>>>>>>> faace65 (Add comprehensive OAuth security, testing, and coverage infrastructure)
        # Should return error response
        self.assertEqual(result, TwitterMockResponses.TOKEN_EXCHANGE_ERROR)
        self.assertIn('error', result)
        self.assertEqual(result['error'], 'invalid_grant')
```

<<<<<<< HEAD
### Reddit-Specific Tests  
=======
### Reddit-Specific Tests
>>>>>>> faace65 (Add comprehensive OAuth security, testing, and coverage infrastructure)
```python
# oauth2_capture/tests/providers/test_reddit.py
from django.test import TestCase
from unittest.mock import patch, Mock
from requests.auth import HTTPBasicAuth

from oauth2_capture.services.oauth2 import RedditOAuth2Provider
from .mock_responses import RedditMockResponses

class RedditProviderTests(TestCase):
<<<<<<< HEAD
    
    def setUp(self):
        self.provider = RedditOAuth2Provider('reddit')
        
=======

    def setUp(self):
        self.provider = RedditOAuth2Provider('reddit')

>>>>>>> faace65 (Add comprehensive OAuth security, testing, and coverage infrastructure)
    def test_authorization_url_includes_duration(self):
        """Test Reddit authorization URL includes permanent duration."""
        auth_url = self.provider.get_authorization_url(
            state='test_state',
            redirect_uri='http://example.com/callback',
            request=None
        )
<<<<<<< HEAD
        
        # Should include duration=permanent for refresh tokens
        self.assertIn('duration=permanent', auth_url)
        self.assertIn('reddit.com/api/v1/authorize', auth_url)
        
=======

        # Should include duration=permanent for refresh tokens
        self.assertIn('duration=permanent', auth_url)
        self.assertIn('reddit.com/api/v1/authorize', auth_url)

>>>>>>> faace65 (Add comprehensive OAuth security, testing, and coverage infrastructure)
    @patch('requests.post')
    def test_token_exchange_uses_basic_auth(self, mock_post):
        """Test Reddit token exchange uses HTTP Basic Auth."""
        mock_post.return_value = Mock(
            json=lambda: RedditMockResponses.TOKEN_EXCHANGE_SUCCESS,
            status_code=200
        )
<<<<<<< HEAD
        
        result = self.provider.exchange_code_for_token(
            code='test_code',
            redirect_uri='http://example.com/callback', 
            request=None
        )
        
        # Should use HTTP Basic Auth
        mock_post.assert_called_once()
        call_args = mock_post.call_args
        
        self.assertIsInstance(call_args[1]['auth'], HTTPBasicAuth)
        
        # Should include User-Agent header
        self.assertIn('User-Agent', call_args[1]['headers'])
        self.assertIn('Oauth2Capture', call_args[1]['headers']['User-Agent'])
        
        # Should NOT include client credentials in data
        self.assertNotIn('client_id', call_args[1]['data'])
        self.assertNotIn('client_secret', call_args[1]['data'])
        
=======

        result = self.provider.exchange_code_for_token(
            code='test_code',
            redirect_uri='http://example.com/callback',
            request=None
        )

        # Should use HTTP Basic Auth
        mock_post.assert_called_once()
        call_args = mock_post.call_args

        self.assertIsInstance(call_args[1]['auth'], HTTPBasicAuth)

        # Should include User-Agent header
        self.assertIn('User-Agent', call_args[1]['headers'])
        self.assertIn('Oauth2Capture', call_args[1]['headers']['User-Agent'])

        # Should NOT include client credentials in data
        self.assertNotIn('client_id', call_args[1]['data'])
        self.assertNotIn('client_secret', call_args[1]['data'])

>>>>>>> faace65 (Add comprehensive OAuth security, testing, and coverage infrastructure)
    @patch('requests.get')
    def test_user_info_uses_oauth_subdomain(self, mock_get):
        """Test Reddit user info uses oauth.reddit.com subdomain."""
        mock_get.return_value = Mock(
            json=lambda: RedditMockResponses.USER_INFO_SUCCESS,
            status_code=200
        )
<<<<<<< HEAD
        
        result = self.provider.get_user_info('test_token')
        
=======

        result = self.provider.get_user_info('test_token')

>>>>>>> faace65 (Add comprehensive OAuth security, testing, and coverage infrastructure)
        # Should use oauth subdomain
        mock_get.assert_called_once()
        call_args = mock_get.call_args
        self.assertIn('oauth.reddit.com', call_args[0][0])
<<<<<<< HEAD
        
        # Should use Bearer token
        self.assertEqual(call_args[1]['headers']['Authorization'], 'Bearer test_token')
        
    @patch('requests.post')  
=======

        # Should use Bearer token
        self.assertEqual(call_args[1]['headers']['Authorization'], 'Bearer test_token')

    @patch('requests.post')
>>>>>>> faace65 (Add comprehensive OAuth security, testing, and coverage infrastructure)
    def test_refresh_token_custom_implementation(self, mock_post):
        """Test Reddit's custom refresh token implementation."""
        mock_post.return_value = Mock(
            json=lambda: RedditMockResponses.TOKEN_EXCHANGE_SUCCESS,
            status_code=200
        )
<<<<<<< HEAD
        
        result = self.provider.refresh_token('test_refresh_token')
        
        # Should use Basic Auth (not in POST data)
        mock_post.assert_called_once()
        call_args = mock_post.call_args
        
        self.assertIsInstance(call_args[1]['auth'], HTTPBasicAuth)
        
        # Should include User-Agent
        self.assertIn('User-Agent', call_args[1]['headers'])
        
=======

        result = self.provider.refresh_token('test_refresh_token')

        # Should use Basic Auth (not in POST data)
        mock_post.assert_called_once()
        call_args = mock_post.call_args

        self.assertIsInstance(call_args[1]['auth'], HTTPBasicAuth)

        # Should include User-Agent
        self.assertIn('User-Agent', call_args[1]['headers'])

>>>>>>> faace65 (Add comprehensive OAuth security, testing, and coverage infrastructure)
        # Data should be minimal (no client credentials)
        expected_data = {
            'grant_type': 'refresh_token',
            'refresh_token': 'test_refresh_token'
        }
        self.assertEqual(call_args[1]['data'], expected_data)
```

### GitHub-Specific Tests
```python
<<<<<<< HEAD
# oauth2_capture/tests/providers/test_github.py  
=======
# oauth2_capture/tests/providers/test_github.py
>>>>>>> faace65 (Add comprehensive OAuth security, testing, and coverage infrastructure)
from django.test import TestCase
from unittest.mock import patch, Mock

from oauth2_capture.services.oauth2 import GitHubOAuth2Provider
from .mock_responses import GitHubMockResponses

class GitHubProviderTests(TestCase):
<<<<<<< HEAD
    
    def setUp(self):
        self.provider = GitHubOAuth2Provider('github')
        
=======

    def setUp(self):
        self.provider = GitHubOAuth2Provider('github')

>>>>>>> faace65 (Add comprehensive OAuth security, testing, and coverage infrastructure)
    @patch('requests.get')
    def test_user_info_token_prefix(self, mock_get):
        """Test GitHub uses 'token' prefix instead of 'Bearer'."""
        mock_get.return_value = Mock(
            json=lambda: GitHubMockResponses.USER_INFO_SUCCESS,
            status_code=200
        )
<<<<<<< HEAD
        
        result = self.provider.get_user_info('test_token')
        
=======

        result = self.provider.get_user_info('test_token')

>>>>>>> faace65 (Add comprehensive OAuth security, testing, and coverage infrastructure)
        # Should use 'token' prefix
        mock_get.assert_called_once()
        call_args = mock_get.call_args
        self.assertEqual(call_args[1]['headers']['Authorization'], 'token test_token')
<<<<<<< HEAD
        
=======

>>>>>>> faace65 (Add comprehensive OAuth security, testing, and coverage infrastructure)
    @patch('requests.get')
    def test_null_name_handling(self, mock_get):
        """Test GitHub null name field handling."""
        mock_get.return_value = Mock(
            json=lambda: GitHubMockResponses.USER_INFO_NULL_NAME,
            status_code=200
        )
<<<<<<< HEAD
        
        result = self.provider.get_user_info('test_token')
        
        # Should replace null name with login
        self.assertEqual(result['name'], 'testuser')
        self.assertEqual(result['login'], 'testuser')
        
=======

        result = self.provider.get_user_info('test_token')

        # Should replace null name with login
        self.assertEqual(result['name'], 'testuser')
        self.assertEqual(result['login'], 'testuser')

>>>>>>> faace65 (Add comprehensive OAuth security, testing, and coverage infrastructure)
    @patch('requests.post')
    def test_token_exchange_headers(self, mock_post):
        """Test GitHub token exchange uses correct headers."""
        mock_post.return_value = Mock(
            json=lambda: GitHubMockResponses.TOKEN_EXCHANGE_SUCCESS,
            status_code=200
        )
<<<<<<< HEAD
        
=======

>>>>>>> faace65 (Add comprehensive OAuth security, testing, and coverage infrastructure)
        result = self.provider.exchange_code_for_token(
            code='test_code',
            redirect_uri='http://example.com/callback',
            request=None
        )
<<<<<<< HEAD
        
        # Should use Accept: application/json header
        mock_post.assert_called_once()
        call_args = mock_post.call_args
        
        self.assertEqual(call_args[1]['headers']['Accept'], 'application/json')
        
=======

        # Should use Accept: application/json header
        mock_post.assert_called_once()
        call_args = mock_post.call_args

        self.assertEqual(call_args[1]['headers']['Accept'], 'application/json')

>>>>>>> faace65 (Add comprehensive OAuth security, testing, and coverage infrastructure)
        # Should include client credentials in data
        self.assertIn('client_id', call_args[1]['data'])
        self.assertIn('client_secret', call_args[1]['data'])
```

## Success Criteria
- [ ] Comprehensive test coverage for each provider's unique characteristics
- [ ] Realistic API response mocks based on actual provider documentation
- [ ] Edge case testing for provider-specific quirks
- [ ] Error handling tests for provider-specific error formats
- [ ] Authentication method verification (Bearer vs token vs Basic Auth)
- [ ] Parameter validation for provider-specific requirements
- [ ] Response parsing tests for provider-specific data structures
<<<<<<< HEAD
- [ ] Integration with core OAuth flow tests
=======
- [ ] Integration with core OAuth flow tests
>>>>>>> faace65 (Add comprehensive OAuth security, testing, and coverage infrastructure)
