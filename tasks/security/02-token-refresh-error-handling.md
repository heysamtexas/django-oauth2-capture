# Token Refresh Error Handling Improvement

## Objective
Improve error handling when token refresh fails in `get_valid_token()` method. Currently, when refresh fails, the method returns `None` without providing clear feedback to the calling application about what went wrong or how to recover.

## Context
The `get_valid_token()` method in `oauth2_capture/services/oauth2.py:202-238` is the primary interface for obtaining valid tokens. When tokens are expired, it attempts refresh, but if refresh fails:

- Returns `None` (line 225)
- Logs an error but doesn't propagate specific error information
- Calling applications have no context about why the token failed
- No clear guidance for applications on how to handle re-authorization

**Current Issues:**
- Generic `None` return provides no context about failure type
- Applications can't distinguish between different failure scenarios
- No structured way to trigger re-authorization flow

## Technical Details

### Failure Scenarios to Handle
1. **Refresh token expired**: User needs to re-authorize
2. **Network/API errors**: Temporary failure, retry may work
3. **Invalid credentials**: Configuration or provider issues
4. **Revoked permissions**: User revoked app access

### Proposed Solution
Create a custom exception hierarchy and modify `get_valid_token()` to raise specific exceptions instead of returning `None`.

### Exception Classes
```python
class TokenError(Exception):
    """Base exception for token-related errors"""
    pass

<<<<<<< HEAD
class TokenRefreshError(TokenError): 
=======
class TokenRefreshError(TokenError):
>>>>>>> faace65 (Add comprehensive OAuth security, testing, and coverage infrastructure)
    """Token refresh failed - may be retryable"""
    pass

class TokenExpiredError(TokenError):
    """Token expired and refresh failed - re-auth required"""
    pass

class TokenRevokedError(TokenError):
    """Token was revoked by user - re-auth required"""
    pass
```

## Testing Requirements
1. **Successful Refresh Test**: Verify normal token refresh continues to work
2. **Network Error Test**: Mock network failure during refresh
<<<<<<< HEAD
3. **Expired Refresh Token Test**: Simulate expired refresh token scenario  
=======
3. **Expired Refresh Token Test**: Simulate expired refresh token scenario
>>>>>>> faace65 (Add comprehensive OAuth security, testing, and coverage infrastructure)
4. **Revoked Token Test**: Mock provider response for revoked token
5. **Exception Propagation Test**: Verify exceptions bubble up correctly
6. **Backward Compatibility Test**: Ensure existing usage patterns still work

## Dependencies
- Consider impact on existing code that expects `None` return
- May want to implement gradually with deprecation warnings

## Estimated Complexity
Medium (half day)

## Files to Modify
- `oauth2_capture/services/oauth2.py`: Modify `get_valid_token()` method (lines 202-238)
- `oauth2_capture/exceptions.py`: Create new file for custom exceptions
- `oauth2_capture/__init__.py`: Export exceptions for easy import
- `development/demo/views.py`: Update demo to handle new exceptions
- `oauth2_capture/tests/services/test_oauth2.py`: Create comprehensive tests

## Example Code

### Custom Exceptions
```python
# oauth2_capture/exceptions.py
class TokenError(Exception):
    """Base exception for token-related errors."""
    def __init__(self, message: str, provider: str = None, recoverable: bool = False):
        super().__init__(message)
        self.provider = provider
        self.recoverable = recoverable

class TokenRefreshError(TokenError):
    """Token refresh failed - may be retryable."""
    def __init__(self, message: str, provider: str = None, response_code: int = None):
        super().__init__(message, provider, recoverable=True)
        self.response_code = response_code

<<<<<<< HEAD
class TokenExpiredError(TokenError): 
=======
class TokenExpiredError(TokenError):
>>>>>>> faace65 (Add comprehensive OAuth security, testing, and coverage infrastructure)
    """Token expired and refresh failed - re-auth required."""
    def __init__(self, message: str, provider: str = None):
        super().__init__(message, provider, recoverable=False)
```

### Modified get_valid_token Method
```python
def get_valid_token(self, oauth_token: OAuthToken) -> str:
    """Get a valid access token, refreshing if necessary.
<<<<<<< HEAD
    
=======

>>>>>>> faace65 (Add comprehensive OAuth security, testing, and coverage infrastructure)
    Raises:
        TokenExpiredError: When token is expired and refresh fails
        TokenRefreshError: When refresh fails due to network/API issues
        TokenRevokedError: When token has been revoked
    """
    if oauth_token.expires_at and oauth_token.expires_at <= timezone.now():
        logger.debug(f"Token for {oauth_token.provider}:{oauth_token.name} has expired. Refreshing...")
<<<<<<< HEAD
        
=======

>>>>>>> faace65 (Add comprehensive OAuth security, testing, and coverage infrastructure)
        try:
            token_data = self.refresh_token(oauth_token.refresh_token)
        except requests.RequestException as e:
            raise TokenRefreshError(
<<<<<<< HEAD
                f"Network error during token refresh: {str(e)}", 
                provider=self.provider_name
            )
        
=======
                f"Network error during token refresh: {str(e)}",
                provider=self.provider_name
            )

>>>>>>> faace65 (Add comprehensive OAuth security, testing, and coverage infrastructure)
        if not token_data or "access_token" not in token_data:
            # Analyze the error response to determine appropriate exception
            if "error" in token_data:
                error_code = token_data.get("error")
                if error_code == "invalid_grant":
                    raise TokenExpiredError(
                        f"Refresh token expired for {oauth_token.provider}:{oauth_token.name}",
                        provider=self.provider_name
                    )
<<<<<<< HEAD
            
=======

>>>>>>> faace65 (Add comprehensive OAuth security, testing, and coverage infrastructure)
            raise TokenRefreshError(
                f"Token refresh failed: {token_data}",
                provider=self.provider_name
            )
<<<<<<< HEAD
        
        # Update token logic remains the same...
    
=======

        # Update token logic remains the same...

>>>>>>> faace65 (Add comprehensive OAuth security, testing, and coverage infrastructure)
    return oauth_token.access_token
```

### Usage in Client Code
```python
# How applications would handle the new exceptions
try:
    token = provider.get_valid_token(oauth_token)
    # Use token for API calls
except TokenExpiredError:
    # Redirect user to re-authorization flow
    return redirect(f'/oauth2/authorize/{provider_name}')
except TokenRefreshError as e:
    if e.recoverable:
        # Maybe retry later or show temporary error
        messages.error(request, "Temporary token issue, please try again")
    else:
        # Handle non-recoverable errors
        messages.error(request, f"Token error: {e}")
```

## Success Criteria
- [ ] Clear exception types for different failure scenarios
- [ ] Structured error information available to calling applications
- [ ] Backward compatibility maintained (with deprecation path)
- [ ] Comprehensive logging of error scenarios
- [ ] Demo application updated to show proper error handling
<<<<<<< HEAD
- [ ] Full test coverage of all error scenarios
=======
- [ ] Full test coverage of all error scenarios
>>>>>>> faace65 (Add comprehensive OAuth security, testing, and coverage infrastructure)
