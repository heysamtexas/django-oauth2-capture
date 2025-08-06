# Re-authentication Flow Documentation

## Objective
Create comprehensive documentation explaining how the oauth2_capture library handles token expiration and re-authentication scenarios, including guidance for application developers on implementing user-friendly re-auth flows.

## Context
Currently, there is limited documentation about what happens when OAuth tokens expire or become invalid. From our conversation, the maintainer mentioned:

> "there are issues of token refresh and re-auth workflows because eventually the oauth tokens expire and the user must reauthorize with the provider"
<<<<<<< HEAD
> 
=======
>
>>>>>>> faace65 (Add comprehensive OAuth security, testing, and coverage infrastructure)
> "I believe we message them and place them into a re-auth flow, but i dont remember. (we should document this)"

**Documentation Gaps:**
- No clear explanation of when re-authorization is needed
- No guidance on detecting token expiration vs revocation
- No examples of implementing user-friendly re-auth flows
- No best practices for handling re-auth in production applications

**Current Behavior Analysis:**
- `get_valid_token()` returns `None` when refresh fails
- Applications must detect `None` return and handle re-auth
- No built-in UI or messaging for re-auth scenarios

## Technical Details

### Re-authentication Scenarios

1. **Token Expiration with Valid Refresh Token**
   - Automatic refresh handled by library
   - No user intervention required
   - Transparent to application

2. **Refresh Token Expiration**
   - Cannot refresh automatically
   - User must re-authorize
   - Application must detect and handle

3. **Token Revocation by User**
   - User revoked app permissions on provider
   - Refresh attempts fail
   - Application must prompt re-authorization

4. **Provider Policy Changes**
   - Scope requirements changed
   - Token format changes
   - Provider-specific issues

5. **Long-term Inactivity**
   - Some providers expire tokens after inactivity
   - May require fresh authorization

### Documentation Structure

1. **Overview**: When and why re-authentication happens
2. **Detection**: How to detect different failure scenarios
3. **Implementation Patterns**: Common approaches for handling re-auth
4. **User Experience**: Best practices for user-friendly flows
5. **Provider-Specific Notes**: Unique behaviors per provider
6. **Testing**: How to test re-auth flows
7. **Troubleshooting**: Common issues and solutions

## Testing Requirements
1. **Documentation Accuracy**: Verify examples work as documented
2. **Code Completeness**: Ensure all example code is functional
3. **Scenario Coverage**: Document all re-auth scenarios
4. **Provider Testing**: Validate provider-specific guidance
5. **User Experience**: Test documented UX patterns

## Dependencies
- Better error responses (security task 04) for specific error codes
- Token refresh error handling (security task 02) for exception types
- Token validation helpers (security task 03) for proactive checking

## Estimated Complexity
Simple (half day)

## Files to Create
- `docs/reauth-flows.md`: Comprehensive re-auth documentation
- `docs/examples/reauth-patterns.py`: Code examples for common patterns
- `development/demo/reauth_example.py`: Complete working example
- `docs/provider-specific-reauth.md`: Provider-specific re-auth behaviors

## Example Documentation

### Main Re-authentication Documentation
```markdown
# docs/reauth-flows.md

# OAuth2 Re-authentication Flows

When OAuth tokens expire or become invalid, users must re-authenticate with the OAuth provider. This document explains when re-authentication is needed and how to implement user-friendly re-auth flows.

## When Re-authentication is Needed

### Automatic Token Refresh (No Re-auth Needed)
When access tokens expire but refresh tokens are still valid, the library automatically refreshes tokens:

```python
from oauth2_capture.services.oauth2 import OAuth2ProviderFactory
from oauth2_capture.models import OAuthToken

# Get user's token
token = OAuthToken.objects.filter(provider='twitter', owner=request.user).first()

# This automatically refreshes if needed
provider = OAuth2ProviderFactory.get_provider('twitter')
access_token = provider.get_valid_token(token)

if access_token:
    # Token is valid (possibly refreshed)
    # Proceed with API call
    pass
```

### Re-authentication Required Scenarios

Re-authentication is required when `get_valid_token()` returns `None`:

1. **Refresh Token Expired**: The refresh token itself has expired
2. **Token Revoked**: User revoked app permissions on the provider
3. **Scope Changes**: App requires additional permissions
4. **Provider Issues**: Provider-specific authentication problems

## Detecting Re-authentication Needs

### Basic Detection Pattern

```python
def get_twitter_token(user):
    """Get valid Twitter token or None if re-auth needed."""
    token = OAuthToken.objects.filter(provider='twitter', owner=user).first()
<<<<<<< HEAD
    
    if not token:
        return None  # No token exists - initial auth needed
    
    provider = OAuth2ProviderFactory.get_provider('twitter')
    access_token = provider.get_valid_token(token)
    
=======

    if not token:
        return None  # No token exists - initial auth needed

    provider = OAuth2ProviderFactory.get_provider('twitter')
    access_token = provider.get_valid_token(token)

>>>>>>> faace65 (Add comprehensive OAuth security, testing, and coverage infrastructure)
    return access_token  # Valid token or None if re-auth needed

# Usage
access_token = get_twitter_token(request.user)
if not access_token:
    # Redirect to re-authentication
    return redirect(f'/oauth2/twitter/authorize/')
```

### Advanced Detection with Error Handling

```python
from oauth2_capture.exceptions import TokenExpiredError, TokenRevokedError

def check_token_status(user, provider_name):
    """Check token status with detailed error information."""
    token = OAuthToken.objects.filter(provider=provider_name, owner=user).first()
<<<<<<< HEAD
    
    if not token:
        return {'status': 'no_token', 'action': 'initial_auth'}
    
    try:
        provider = OAuth2ProviderFactory.get_provider(provider_name)
        access_token = provider.get_valid_token(token)
        
=======

    if not token:
        return {'status': 'no_token', 'action': 'initial_auth'}

    try:
        provider = OAuth2ProviderFactory.get_provider(provider_name)
        access_token = provider.get_valid_token(token)

>>>>>>> faace65 (Add comprehensive OAuth security, testing, and coverage infrastructure)
        if access_token:
            return {'status': 'valid', 'token': access_token}
        else:
            return {'status': 'refresh_failed', 'action': 'reauth'}
<<<<<<< HEAD
            
=======

>>>>>>> faace65 (Add comprehensive OAuth security, testing, and coverage infrastructure)
    except TokenExpiredError:
        return {'status': 'expired', 'action': 'reauth', 'reason': 'expired_refresh_token'}
    except TokenRevokedError:
        return {'status': 'revoked', 'action': 'reauth', 'reason': 'user_revoked'}
    except Exception as e:
        return {'status': 'error', 'action': 'reauth', 'reason': str(e)}

# Usage
status = check_token_status(request.user, 'twitter')
if status['action'] == 'reauth':
    messages.warning(request, f"Please reconnect your Twitter account: {status['reason']}")
    return redirect('/oauth2/twitter/authorize/')
```

## Implementation Patterns

### Pattern 1: Decorator for Token Validation

```python
from functools import wraps
from django.shortcuts import redirect
from django.contrib import messages

def require_oauth_token(provider_name, redirect_url=None):
    """Decorator to ensure valid OAuth token exists."""
    def decorator(view_func):
        @wraps(view_func)
        def wrapper(request, *args, **kwargs):
            token = OAuthToken.objects.filter(
<<<<<<< HEAD
                provider=provider_name, 
                owner=request.user
            ).first()
            
            if not token:
                messages.info(request, f'Please connect your {provider_name.title()} account')
                return redirect(redirect_url or f'/oauth2/{provider_name}/authorize/')
            
            provider = OAuth2ProviderFactory.get_provider(provider_name)
            access_token = provider.get_valid_token(token)
            
            if not access_token:
                messages.warning(
                    request, 
                    f'Your {provider_name.title()} connection has expired. Please reconnect.'
                )
                return redirect(redirect_url or f'/oauth2/{provider_name}/authorize/')
            
            # Add token to request for use in view
            request.oauth_token = access_token
            return view_func(request, *args, **kwargs)
        
=======
                provider=provider_name,
                owner=request.user
            ).first()

            if not token:
                messages.info(request, f'Please connect your {provider_name.title()} account')
                return redirect(redirect_url or f'/oauth2/{provider_name}/authorize/')

            provider = OAuth2ProviderFactory.get_provider(provider_name)
            access_token = provider.get_valid_token(token)

            if not access_token:
                messages.warning(
                    request,
                    f'Your {provider_name.title()} connection has expired. Please reconnect.'
                )
                return redirect(redirect_url or f'/oauth2/{provider_name}/authorize/')

            # Add token to request for use in view
            request.oauth_token = access_token
            return view_func(request, *args, **kwargs)

>>>>>>> faace65 (Add comprehensive OAuth security, testing, and coverage infrastructure)
        return wrapper
    return decorator

# Usage
@require_oauth_token('twitter')
def post_to_twitter(request):
    """Post to Twitter - token guaranteed to be valid."""
    # Use request.oauth_token for API calls
    pass
```

### Pattern 2: Service Class with Re-auth Handling

```python
class SocialMediaService:
    """Service for social media operations with re-auth handling."""
<<<<<<< HEAD
    
    def __init__(self, user):
        self.user = user
    
=======

    def __init__(self, user):
        self.user = user

>>>>>>> faace65 (Add comprehensive OAuth security, testing, and coverage infrastructure)
    def post_to_provider(self, provider_name, content):
        """Post content to provider with automatic re-auth detection."""
        try:
            token = self._get_valid_token(provider_name)
            if not token:
                return {
                    'success': False,
                    'error': 'reauth_required',
                    'reauth_url': f'/oauth2/{provider_name}/authorize/',
                    'message': f'Please reconnect your {provider_name.title()} account'
                }
<<<<<<< HEAD
            
            # Proceed with posting
            result = self._perform_post(provider_name, token, content)
            return {'success': True, 'result': result}
            
=======

            # Proceed with posting
            result = self._perform_post(provider_name, token, content)
            return {'success': True, 'result': result}

>>>>>>> faace65 (Add comprehensive OAuth security, testing, and coverage infrastructure)
        except Exception as e:
            return {
                'success': False,
                'error': 'api_error',
                'message': str(e)
            }
<<<<<<< HEAD
    
    def _get_valid_token(self, provider_name):
        """Get valid token or None if re-auth needed."""
        token = OAuthToken.objects.filter(
            provider=provider_name, 
            owner=self.user
        ).first()
        
        if not token:
            return None
        
        provider = OAuth2ProviderFactory.get_provider(provider_name)
        return provider.get_valid_token(token)
    
=======

    def _get_valid_token(self, provider_name):
        """Get valid token or None if re-auth needed."""
        token = OAuthToken.objects.filter(
            provider=provider_name,
            owner=self.user
        ).first()

        if not token:
            return None

        provider = OAuth2ProviderFactory.get_provider(provider_name)
        return provider.get_valid_token(token)

>>>>>>> faace65 (Add comprehensive OAuth security, testing, and coverage infrastructure)
    def _perform_post(self, provider_name, token, content):
        """Perform the actual post operation."""
        # Implementation depends on provider
        pass

# Usage in views
def social_post_view(request):
    service = SocialMediaService(request.user)
    result = service.post_to_provider('twitter', 'Hello world!')
<<<<<<< HEAD
    
=======

>>>>>>> faace65 (Add comprehensive OAuth security, testing, and coverage infrastructure)
    if not result['success']:
        if result['error'] == 'reauth_required':
            return redirect(result['reauth_url'])
        else:
            messages.error(request, result['message'])
    else:
        messages.success(request, 'Posted successfully!')
<<<<<<< HEAD
    
=======

>>>>>>> faace65 (Add comprehensive OAuth security, testing, and coverage infrastructure)
    return redirect('/')
```

### Pattern 3: Middleware for Global Token Checking

```python
from django.utils.deprecation import MiddlewareMixin

class OAuth2ReauthMiddleware(MiddlewareMixin):
    """Middleware to add OAuth token status to all requests."""
<<<<<<< HEAD
    
    def process_request(self, request):
        if request.user.is_authenticated:
            request.oauth_status = self._check_all_tokens(request.user)
    
=======

    def process_request(self, request):
        if request.user.is_authenticated:
            request.oauth_status = self._check_all_tokens(request.user)

>>>>>>> faace65 (Add comprehensive OAuth security, testing, and coverage infrastructure)
    def _check_all_tokens(self, user):
        """Check status of all user's OAuth tokens."""
        tokens = OAuthToken.objects.filter(owner=user)
        status = {}
<<<<<<< HEAD
        
        for token in tokens:
            provider = OAuth2ProviderFactory.get_provider(token.provider)
            access_token = provider.get_valid_token(token)
            
=======

        for token in tokens:
            provider = OAuth2ProviderFactory.get_provider(token.provider)
            access_token = provider.get_valid_token(token)

>>>>>>> faace65 (Add comprehensive OAuth security, testing, and coverage infrastructure)
            status[token.provider] = {
                'valid': access_token is not None,
                'reauth_url': f'/oauth2/{token.provider}/authorize/' if not access_token else None
            }
<<<<<<< HEAD
        
=======

>>>>>>> faace65 (Add comprehensive OAuth security, testing, and coverage infrastructure)
        return status

# Usage in templates
{% if request.oauth_status.twitter and not request.oauth_status.twitter.valid %}
    <div class="alert alert-warning">
<<<<<<< HEAD
        Your Twitter connection has expired. 
=======
        Your Twitter connection has expired.
>>>>>>> faace65 (Add comprehensive OAuth security, testing, and coverage infrastructure)
        <a href="{{ request.oauth_status.twitter.reauth_url }}">Reconnect</a>
    </div>
{% endif %}
```

## User Experience Best Practices

### 1. Clear Messaging

```python
# Good: Specific, actionable messages
<<<<<<< HEAD
messages.warning(request, 
    'Your Twitter connection has expired. Click here to reconnect and continue posting.'
)

# Bad: Generic, unclear messages  
=======
messages.warning(request,
    'Your Twitter connection has expired. Click here to reconnect and continue posting.'
)

# Bad: Generic, unclear messages
>>>>>>> faace65 (Add comprehensive OAuth security, testing, and coverage infrastructure)
messages.error(request, 'Authentication failed')
```

### 2. Contextual Re-auth

```python
def handle_reauth_needed(request, provider, original_action):
    """Handle re-auth with context about what user was trying to do."""
<<<<<<< HEAD
    
=======

>>>>>>> faace65 (Add comprehensive OAuth security, testing, and coverage infrastructure)
    # Store the original action in session
    request.session['pending_action'] = {
        'type': original_action,
        'provider': provider,
        'timestamp': timezone.now().isoformat()
    }
<<<<<<< HEAD
    
    messages.info(request, 
        f'To {original_action}, please reconnect your {provider.title()} account.'
    )
    
=======

    messages.info(request,
        f'To {original_action}, please reconnect your {provider.title()} account.'
    )

>>>>>>> faace65 (Add comprehensive OAuth security, testing, and coverage infrastructure)
    return redirect(f'/oauth2/{provider}/authorize/')

def oauth_callback_with_context(request, provider):
    """OAuth callback that handles pending actions."""
<<<<<<< HEAD
    
    # Handle normal OAuth callback
    response = oauth2_callback(request, provider)
    
=======

    # Handle normal OAuth callback
    response = oauth2_callback(request, provider)

>>>>>>> faace65 (Add comprehensive OAuth security, testing, and coverage infrastructure)
    # Check for pending actions
    pending = request.session.get('pending_action')
    if pending and pending['provider'] == provider:
        del request.session['pending_action']
<<<<<<< HEAD
        
        messages.success(request, 
            f'{provider.title()} reconnected! You can now {pending["type"]}.'
        )
        
        # Redirect to original action or appropriate page
        return redirect('/')
    
=======

        messages.success(request,
            f'{provider.title()} reconnected! You can now {pending["type"]}.'
        )

        # Redirect to original action or appropriate page
        return redirect('/')

>>>>>>> faace65 (Add comprehensive OAuth security, testing, and coverage infrastructure)
    return response
```

### 3. Proactive Token Monitoring

```python
def dashboard_view(request):
    """Dashboard that shows token status proactively."""
<<<<<<< HEAD
    
=======

>>>>>>> faace65 (Add comprehensive OAuth security, testing, and coverage infrastructure)
    if request.user.is_authenticated:
        # Check all tokens and warn about upcoming expirations
        tokens = OAuthToken.objects.filter(owner=request.user)
        warnings = []
<<<<<<< HEAD
        
        for token in tokens:
            if token.expires_at:
                time_until_expiry = token.expires_at - timezone.now()
                
=======

        for token in tokens:
            if token.expires_at:
                time_until_expiry = token.expires_at - timezone.now()

>>>>>>> faace65 (Add comprehensive OAuth security, testing, and coverage infrastructure)
                if time_until_expiry < timedelta(days=7):
                    warnings.append({
                        'provider': token.provider,
                        'expires_in_days': time_until_expiry.days,
                        'reauth_url': f'/oauth2/{token.provider}/authorize/'
                    })
<<<<<<< HEAD
        
=======

>>>>>>> faace65 (Add comprehensive OAuth security, testing, and coverage infrastructure)
        if warnings:
            context = {'token_warnings': warnings}
        else:
            context = {}
<<<<<<< HEAD
    
=======

>>>>>>> faace65 (Add comprehensive OAuth security, testing, and coverage infrastructure)
    return render(request, 'dashboard.html', context)
```

## Provider-Specific Behaviors

### Twitter
- **Refresh Token Lifetime**: Long-lived but can be revoked
- **Common Re-auth Triggers**: User changes password, account suspension
- **Rate Limiting**: May affect refresh attempts

<<<<<<< HEAD
### GitHub  
=======
### GitHub
>>>>>>> faace65 (Add comprehensive OAuth security, testing, and coverage infrastructure)
- **Token Expiration**: Tokens don't expire by default for OAuth apps
- **Re-auth Triggers**: User revokes app access, org policies change
- **Scope Changes**: New permissions require re-authorization

### LinkedIn
- **Token Lifetime**: 60 days by default
<<<<<<< HEAD
- **Refresh Behavior**: Automatic refresh extends lifetime  
=======
- **Refresh Behavior**: Automatic refresh extends lifetime
>>>>>>> faace65 (Add comprehensive OAuth security, testing, and coverage infrastructure)
- **Re-auth Triggers**: Membership changes, privacy settings

### Reddit
- **Token Lifetime**: 1 hour for access tokens
- **Refresh Required**: Very frequent refresh needed
- **Re-auth Triggers**: User account suspension, subreddit bans

## Testing Re-authentication Flows

### Manual Testing

1. **Simulate Token Expiration**: Manually set `expires_at` to past date
2. **Revoke on Provider**: Go to provider settings and revoke app access
3. **Delete Refresh Token**: Set `refresh_token` to empty string
4. **Network Issues**: Mock network failures during refresh

### Automated Testing

```python
class ReauthFlowTests(TestCase):
<<<<<<< HEAD
    
    def test_expired_token_triggers_reauth(self):
        """Test that expired tokens trigger re-authentication."""
        user = User.objects.create_user('testuser')
        
=======

    def test_expired_token_triggers_reauth(self):
        """Test that expired tokens trigger re-authentication."""
        user = User.objects.create_user('testuser')

>>>>>>> faace65 (Add comprehensive OAuth security, testing, and coverage infrastructure)
        # Create expired token
        expired_token = OAuthToken.objects.create(
            provider='twitter',
            user_id='12345',
            owner=user,
            access_token='expired_token',
            expires_at=timezone.now() - timedelta(hours=1)
        )
<<<<<<< HEAD
        
        provider = OAuth2ProviderFactory.get_provider('twitter')
        
        with patch.object(provider, 'refresh_token') as mock_refresh:
            mock_refresh.return_value = {}  # Empty response = failed refresh
            
            result = provider.get_valid_token(expired_token)
            
=======

        provider = OAuth2ProviderFactory.get_provider('twitter')

        with patch.object(provider, 'refresh_token') as mock_refresh:
            mock_refresh.return_value = {}  # Empty response = failed refresh

            result = provider.get_valid_token(expired_token)

>>>>>>> faace65 (Add comprehensive OAuth security, testing, and coverage infrastructure)
            self.assertIsNone(result)
            mock_refresh.assert_called_once()
```

## Troubleshooting Common Issues

### Issue: Infinite Re-auth Loops
**Cause**: OAuth callback creates token but immediately expires
**Solution**: Check system clock, provider configuration

### Issue: Users Not Seeing Re-auth Messages
**Cause**: Messages not displayed in template
**Solution**: Ensure messages framework is properly configured

<<<<<<< HEAD
### Issue: Re-auth Required After Each Request  
=======
### Issue: Re-auth Required After Each Request
>>>>>>> faace65 (Add comprehensive OAuth security, testing, and coverage infrastructure)
**Cause**: Token refresh failing silently
**Solution**: Enable debug logging, check provider credentials

### Issue: Different Behavior Across Providers
**Cause**: Provider-specific token lifetimes and refresh behaviors
**Solution**: Implement provider-specific handling, document differences

## Best Practices Summary

1. **Always check token validity** before making API calls
2. **Provide clear, actionable messages** when re-auth is needed
3. **Store context** about what the user was trying to accomplish
4. **Monitor token health** proactively
5. **Test re-auth flows** regularly
6. **Document provider-specific behaviors** for your use case
7. **Handle edge cases** gracefully (network errors, provider downtime)
8. **Consider user experience** - minimize interruptions while maintaining security
```

### Code Examples File
```python
# docs/examples/reauth-patterns.py

"""
Complete examples of re-authentication patterns for oauth2_capture library.

These examples demonstrate different approaches to handling OAuth token
expiration and re-authentication in Django applications.
"""

from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from datetime import timedelta
from functools import wraps

from oauth2_capture.models import OAuthToken
from oauth2_capture.services.oauth2 import OAuth2ProviderFactory

# Example 1: Simple re-auth check function
def needs_reauth(user, provider_name):
    """
    Check if user needs to re-authenticate with a provider.
<<<<<<< HEAD
    
=======

>>>>>>> faace65 (Add comprehensive OAuth security, testing, and coverage infrastructure)
    Returns:
        bool: True if re-authentication is needed, False if token is valid
    """
    token = OAuthToken.objects.filter(provider=provider_name, owner=user).first()
<<<<<<< HEAD
    
    if not token:
        return True  # No token exists
    
    provider = OAuth2ProviderFactory.get_provider(provider_name)
    access_token = provider.get_valid_token(token)
    
=======

    if not token:
        return True  # No token exists

    provider = OAuth2ProviderFactory.get_provider(provider_name)
    access_token = provider.get_valid_token(token)

>>>>>>> faace65 (Add comprehensive OAuth security, testing, and coverage infrastructure)
    return access_token is None

# Example 2: View decorator for required OAuth tokens
def oauth_required(provider_name, redirect_to=None):
    """
    Decorator that ensures a valid OAuth token exists for the provider.
    Redirects to OAuth authorization if re-auth is needed.
    """
    def decorator(view_func):
        @wraps(view_func)
        def wrapper(request, *args, **kwargs):
            if not request.user.is_authenticated:
                return redirect('login')
<<<<<<< HEAD
            
=======

>>>>>>> faace65 (Add comprehensive OAuth security, testing, and coverage infrastructure)
            if needs_reauth(request.user, provider_name):
                messages.warning(
                    request,
                    f'Please connect your {provider_name.title()} account to continue.'
                )
                redirect_url = redirect_to or f'/oauth2/{provider_name}/authorize/'
                return redirect(redirect_url)
<<<<<<< HEAD
            
=======

>>>>>>> faace65 (Add comprehensive OAuth security, testing, and coverage infrastructure)
            return view_func(request, *args, **kwargs)
        return wrapper
    return decorator

# Example 3: Service class with comprehensive error handling
class SocialPostingService:
    """Service for posting to social media with re-auth handling."""
<<<<<<< HEAD
    
    def __init__(self, user):
        self.user = user
    
    def post_content(self, provider_name, content):
        """
        Post content to a social media provider.
        
=======

    def __init__(self, user):
        self.user = user

    def post_content(self, provider_name, content):
        """
        Post content to a social media provider.

>>>>>>> faace65 (Add comprehensive OAuth security, testing, and coverage infrastructure)
        Returns dict with success status and any required actions.
        """
        try:
            # Get valid token
            token_result = self._get_token_status(provider_name)
<<<<<<< HEAD
            
=======

>>>>>>> faace65 (Add comprehensive OAuth security, testing, and coverage infrastructure)
            if not token_result['valid']:
                return {
                    'success': False,
                    'action_required': 'reauth',
                    'reauth_url': f'/oauth2/{provider_name}/authorize/',
                    'message': token_result['message']
                }
<<<<<<< HEAD
            
            # Simulate posting (replace with actual API calls)
            post_result = self._make_api_post(provider_name, token_result['token'], content)
            
=======

            # Simulate posting (replace with actual API calls)
            post_result = self._make_api_post(provider_name, token_result['token'], content)

>>>>>>> faace65 (Add comprehensive OAuth security, testing, and coverage infrastructure)
            return {
                'success': True,
                'post_id': post_result['id'],
                'message': f'Successfully posted to {provider_name.title()}'
            }
<<<<<<< HEAD
            
=======

>>>>>>> faace65 (Add comprehensive OAuth security, testing, and coverage infrastructure)
        except Exception as e:
            return {
                'success': False,
                'action_required': 'retry',
                'message': f'Error posting to {provider_name}: {str(e)}'
            }
<<<<<<< HEAD
    
    def _get_token_status(self, provider_name):
        """Get detailed token status."""
        token = OAuthToken.objects.filter(provider=provider_name, owner=self.user).first()
        
=======

    def _get_token_status(self, provider_name):
        """Get detailed token status."""
        token = OAuthToken.objects.filter(provider=provider_name, owner=self.user).first()

>>>>>>> faace65 (Add comprehensive OAuth security, testing, and coverage infrastructure)
        if not token:
            return {
                'valid': False,
                'message': f'No {provider_name.title()} account connected'
            }
<<<<<<< HEAD
        
        provider = OAuth2ProviderFactory.get_provider(provider_name)
        access_token = provider.get_valid_token(token)
        
=======

        provider = OAuth2ProviderFactory.get_provider(provider_name)
        access_token = provider.get_valid_token(token)

>>>>>>> faace65 (Add comprehensive OAuth security, testing, and coverage infrastructure)
        if access_token:
            return {
                'valid': True,
                'token': access_token
            }
        else:
            return {
                'valid': False,
                'message': f'{provider_name.title()} connection expired'
            }
<<<<<<< HEAD
    
=======

>>>>>>> faace65 (Add comprehensive OAuth security, testing, and coverage infrastructure)
    def _make_api_post(self, provider_name, token, content):
        """Make actual API post (implement per provider)."""
        # This would contain provider-specific API calls
        return {'id': '12345', 'url': 'https://example.com/post/12345'}

# Example 4: Views using the service
@login_required
def post_to_social(request):
    """Handle social media posting with re-auth."""
    if request.method == 'POST':
        provider = request.POST.get('provider')
        content = request.POST.get('content')
<<<<<<< HEAD
        
        service = SocialPostingService(request.user)
        result = service.post_content(provider, content)
        
=======

        service = SocialPostingService(request.user)
        result = service.post_content(provider, content)

>>>>>>> faace65 (Add comprehensive OAuth security, testing, and coverage infrastructure)
        if result['success']:
            messages.success(request, result['message'])
        else:
            if result['action_required'] == 'reauth':
                # Store the content to retry after re-auth
                request.session['pending_post'] = {
                    'provider': provider,
                    'content': content
                }
                messages.warning(request, result['message'])
                return redirect(result['reauth_url'])
            else:
                messages.error(request, result['message'])
<<<<<<< HEAD
    
=======

>>>>>>> faace65 (Add comprehensive OAuth security, testing, and coverage infrastructure)
    return render(request, 'social_post.html')

@login_required
def oauth_callback_handler(request, provider):
    """Enhanced OAuth callback that handles pending actions."""
    # First, handle the normal OAuth callback
    from oauth2_capture.views import oauth2_callback
    response = oauth2_callback(request, provider)
<<<<<<< HEAD
    
    # If callback was successful, check for pending actions
    if response.status_code == 200 and 'pending_post' in request.session:
        pending = request.session['pending_post']
        
        if pending['provider'] == provider:
            # Remove from session
            del request.session['pending_post']
            
            # Retry the original post
            service = SocialPostingService(request.user)
            result = service.post_content(provider, pending['content'])
            
=======

    # If callback was successful, check for pending actions
    if response.status_code == 200 and 'pending_post' in request.session:
        pending = request.session['pending_post']

        if pending['provider'] == provider:
            # Remove from session
            del request.session['pending_post']

            # Retry the original post
            service = SocialPostingService(request.user)
            result = service.post_content(provider, pending['content'])

>>>>>>> faace65 (Add comprehensive OAuth security, testing, and coverage infrastructure)
            if result['success']:
                messages.success(request, f"Connected and posted: {result['message']}")
            else:
                messages.warning(request, f"Connected but posting failed: {result['message']}")
<<<<<<< HEAD
    
=======

>>>>>>> faace65 (Add comprehensive OAuth security, testing, and coverage infrastructure)
    return response

# Example 5: Proactive token health checking
@login_required
def dashboard_view(request):
    """Dashboard view with proactive token health monitoring."""
<<<<<<< HEAD
    
    token_status = {}
    expiring_soon = []
    
    # Check all user's tokens
    tokens = OAuthToken.objects.filter(owner=request.user)
    
    for token in tokens:
        provider = OAuth2ProviderFactory.get_provider(token.provider)
        access_token = provider.get_valid_token(token)
        
=======

    token_status = {}
    expiring_soon = []

    # Check all user's tokens
    tokens = OAuthToken.objects.filter(owner=request.user)

    for token in tokens:
        provider = OAuth2ProviderFactory.get_provider(token.provider)
        access_token = provider.get_valid_token(token)

>>>>>>> faace65 (Add comprehensive OAuth security, testing, and coverage infrastructure)
        is_valid = access_token is not None
        token_status[token.provider] = {
            'valid': is_valid,
            'reauth_url': f'/oauth2/{token.provider}/authorize/'
        }
<<<<<<< HEAD
        
        # Check for upcoming expiration (if token has expiry)
        if token.expires_at and is_valid:
            time_until_expiry = token.expires_at - timezone.now()
            
=======

        # Check for upcoming expiration (if token has expiry)
        if token.expires_at and is_valid:
            time_until_expiry = token.expires_at - timezone.now()

>>>>>>> faace65 (Add comprehensive OAuth security, testing, and coverage infrastructure)
            if time_until_expiry < timedelta(days=7):
                expiring_soon.append({
                    'provider': token.provider,
                    'days_remaining': max(0, time_until_expiry.days),
                    'reauth_url': f'/oauth2/{token.provider}/authorize/'
                })
<<<<<<< HEAD
    
=======

>>>>>>> faace65 (Add comprehensive OAuth security, testing, and coverage infrastructure)
    context = {
        'token_status': token_status,
        'expiring_soon': expiring_soon
    }
<<<<<<< HEAD
    
=======

>>>>>>> faace65 (Add comprehensive OAuth security, testing, and coverage infrastructure)
    return render(request, 'dashboard.html', context)

# Example 6: Bulk operation with re-auth handling
@login_required
def bulk_social_post(request):
    """Post to multiple social media platforms with individual re-auth handling."""
    if request.method == 'POST':
        content = request.POST.get('content')
        selected_providers = request.POST.getlist('providers')
<<<<<<< HEAD
        
        service = SocialPostingService(request.user)
        results = {}
        reauth_needed = []
        
        for provider in selected_providers:
            result = service.post_content(provider, content)
            results[provider] = result
            
=======

        service = SocialPostingService(request.user)
        results = {}
        reauth_needed = []

        for provider in selected_providers:
            result = service.post_content(provider, content)
            results[provider] = result

>>>>>>> faace65 (Add comprehensive OAuth security, testing, and coverage infrastructure)
            if not result['success'] and result['action_required'] == 'reauth':
                reauth_needed.append({
                    'provider': provider,
                    'url': result['reauth_url']
                })
<<<<<<< HEAD
        
        # Handle results
        successful_posts = [p for p, r in results.items() if r['success']]
        failed_posts = [p for p, r in results.items() if not r['success'] and r['action_required'] != 'reauth']
        
        if successful_posts:
            messages.success(request, f"Posted to: {', '.join(successful_posts)}")
        
        if failed_posts:
            messages.error(request, f"Failed to post to: {', '.join(failed_posts)}")
        
=======

        # Handle results
        successful_posts = [p for p, r in results.items() if r['success']]
        failed_posts = [p for p, r in results.items() if not r['success'] and r['action_required'] != 'reauth']

        if successful_posts:
            messages.success(request, f"Posted to: {', '.join(successful_posts)}")

        if failed_posts:
            messages.error(request, f"Failed to post to: {', '.join(failed_posts)}")

>>>>>>> faace65 (Add comprehensive OAuth security, testing, and coverage infrastructure)
        if reauth_needed:
            # Store bulk post info for after re-auth
            request.session['pending_bulk_post'] = {
                'content': content,
                'providers': [item['provider'] for item in reauth_needed]
            }
<<<<<<< HEAD
            
            messages.warning(
                request, 
                f"Please reconnect: {', '.join([item['provider'] for item in reauth_needed])}"
            )
            
            # Redirect to first provider that needs re-auth
            return redirect(reauth_needed[0]['url'])
    
=======

            messages.warning(
                request,
                f"Please reconnect: {', '.join([item['provider'] for item in reauth_needed])}"
            )

            # Redirect to first provider that needs re-auth
            return redirect(reauth_needed[0]['url'])

>>>>>>> faace65 (Add comprehensive OAuth security, testing, and coverage infrastructure)
    return render(request, 'bulk_post.html')

# Example 7: Middleware for global token status
class TokenHealthMiddleware:
    """Middleware that adds token health info to all requests."""
<<<<<<< HEAD
    
    def __init__(self, get_response):
        self.get_response = get_response
    
    def __call__(self, request):
        if request.user.is_authenticated:
            request.oauth_health = self._check_token_health(request.user)
        
        response = self.get_response(request)
        return response
    
=======

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated:
            request.oauth_health = self._check_token_health(request.user)

        response = self.get_response(request)
        return response

>>>>>>> faace65 (Add comprehensive OAuth security, testing, and coverage infrastructure)
    def _check_token_health(self, user):
        """Check health of all user tokens."""
        tokens = OAuthToken.objects.filter(owner=user)
        health = {'providers': {}, 'alerts': []}
<<<<<<< HEAD
        
=======

>>>>>>> faace65 (Add comprehensive OAuth security, testing, and coverage infrastructure)
        for token in tokens:
            try:
                provider = OAuth2ProviderFactory.get_provider(token.provider)
                access_token = provider.get_valid_token(token)
<<<<<<< HEAD
                
=======

>>>>>>> faace65 (Add comprehensive OAuth security, testing, and coverage infrastructure)
                is_healthy = access_token is not None
                health['providers'][token.provider] = {
                    'healthy': is_healthy,
                    'reauth_url': f'/oauth2/{token.provider}/authorize/' if not is_healthy else None
                }
<<<<<<< HEAD
                
=======

>>>>>>> faace65 (Add comprehensive OAuth security, testing, and coverage infrastructure)
                if not is_healthy:
                    health['alerts'].append({
                        'type': 'reauth_needed',
                        'provider': token.provider,
                        'message': f'{token.provider.title()} connection needs renewal'
                    })
<<<<<<< HEAD
                
=======

>>>>>>> faace65 (Add comprehensive OAuth security, testing, and coverage infrastructure)
            except Exception as e:
                health['providers'][token.provider] = {
                    'healthy': False,
                    'error': str(e),
                    'reauth_url': f'/oauth2/{token.provider}/authorize/'
                }
<<<<<<< HEAD
        
=======

>>>>>>> faace65 (Add comprehensive OAuth security, testing, and coverage infrastructure)
        return health
```

## Success Criteria
- [ ] Comprehensive documentation of all re-auth scenarios
- [ ] Clear implementation patterns for common use cases
- [ ] Working code examples for each pattern
- [ ] Provider-specific behavior documentation
- [ ] User experience best practices
- [ ] Testing strategies for re-auth flows
- [ ] Troubleshooting guide for common issues
<<<<<<< HEAD
- [ ] Integration examples with Django features
=======
- [ ] Integration examples with Django features
>>>>>>> faace65 (Add comprehensive OAuth security, testing, and coverage infrastructure)
