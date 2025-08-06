# Better Error Responses and Status Codes

## Objective
Replace generic 400 error responses with specific, actionable error messages and appropriate HTTP status codes. Currently, most errors return generic `HttpResponse("Failed to...", status=400)` which provides little context for debugging or user experience.

## Context
Current error handling in `oauth2_capture/views.py` has several issues:

**Generic Error Responses:**
- Line 31: `return HttpResponse(str(e), status=400)` - Just returns exception message
- Line 56-57: `return HttpResponse("Failed to connect {provider} account.", status=400)` - Very generic
- Line 74: `return HttpResponse(str(e), status=400)` - Same pattern repeated

**Missing Error Context:**
- No structured error information
- No error codes for programmatic handling
- No guidance on how to resolve issues
- Same HTTP status code (400) for different error types

## Technical Details

### Error Response Structure
Create a structured error response format that includes:
- Specific error codes
<<<<<<< HEAD
- Human-readable messages  
=======
- Human-readable messages
>>>>>>> faace65 (Add comprehensive OAuth security, testing, and coverage infrastructure)
- Technical details for debugging
- Suggested actions for resolution

### HTTP Status Code Mapping
- `400 Bad Request`: Invalid request parameters
- `401 Unauthorized`: Authentication required
- `403 Forbidden`: Permission denied/scope issues
- `404 Not Found`: Provider not supported
- `500 Internal Server Error`: Server/configuration issues
- `502 Bad Gateway`: Provider API issues
- `503 Service Unavailable`: Temporary provider issues

### Error Categories
1. **Configuration Errors**: Missing client_id/secret, unsupported provider
2. **OAuth Flow Errors**: Invalid/expired authorization codes, state mismatch
3. **Provider API Errors**: Network issues, API rate limits, provider downtime
4. **Permission Errors**: Insufficient scopes, revoked permissions
5. **Validation Errors**: Invalid parameters, malformed requests

## Testing Requirements
1. **Error Response Format Test**: Verify structured error responses
2. **Status Code Test**: Verify appropriate HTTP status codes for each error type
3. **Provider Error Test**: Test handling of provider-specific errors
4. **Configuration Error Test**: Test missing configuration scenarios
5. **Network Error Test**: Test provider API failures
6. **Content Type Test**: Verify JSON responses for API clients

## Dependencies
- Consider backward compatibility with existing error handling
- May need to update client code that expects simple text responses

## Estimated Complexity
Simple (2-3 hours)

## Files to Modify
- `oauth2_capture/views.py`: Replace all error responses (lines 31, 56-57, 74)
- `oauth2_capture/exceptions.py`: Create structured error classes (if not created in task 02)
- `oauth2_capture/templates/oauth2_capture/error.html`: Create error page template
- `oauth2_capture/tests/test_error_responses.py`: Create comprehensive error response tests

## Example Code

### Structured Error Response Helper
```python
# oauth2_capture/responses.py
from django.http import JsonResponse, HttpResponse
from django.template.loader import render_to_string
import json

class ErrorResponse:
    """Structured error response helper."""
<<<<<<< HEAD
    
    def __init__(self, error_code: str, message: str, details: str = None, 
=======

    def __init__(self, error_code: str, message: str, details: str = None,
>>>>>>> faace65 (Add comprehensive OAuth security, testing, and coverage infrastructure)
                 status_code: int = 400, suggested_action: str = None):
        self.error_code = error_code
        self.message = message
        self.details = details
        self.status_code = status_code
        self.suggested_action = suggested_action
<<<<<<< HEAD
    
=======

>>>>>>> faace65 (Add comprehensive OAuth security, testing, and coverage infrastructure)
    def as_json(self) -> JsonResponse:
        """Return error as JSON response."""
        data = {
            'error': {
                'code': self.error_code,
                'message': self.message,
                'status_code': self.status_code
            }
        }
<<<<<<< HEAD
        
=======

>>>>>>> faace65 (Add comprehensive OAuth security, testing, and coverage infrastructure)
        if self.details:
            data['error']['details'] = self.details
        if self.suggested_action:
            data['error']['suggested_action'] = self.suggested_action
<<<<<<< HEAD
            
        return JsonResponse(data, status=self.status_code)
    
=======

        return JsonResponse(data, status=self.status_code)

>>>>>>> faace65 (Add comprehensive OAuth security, testing, and coverage infrastructure)
    def as_html(self, request) -> HttpResponse:
        """Return error as HTML response."""
        context = {
            'error_code': self.error_code,
            'message': self.message,
            'details': self.details,
            'suggested_action': self.suggested_action,
            'status_code': self.status_code
        }
<<<<<<< HEAD
        
        html = render_to_string('oauth2_capture/error.html', context, request)
        return HttpResponse(html, status=self.status_code)
    
=======

        html = render_to_string('oauth2_capture/error.html', context, request)
        return HttpResponse(html, status=self.status_code)

>>>>>>> faace65 (Add comprehensive OAuth security, testing, and coverage infrastructure)
    def auto_response(self, request):
        """Return appropriate response type based on request."""
        if request.headers.get('Accept', '').startswith('application/json'):
            return self.as_json()
        else:
            return self.as_html(request)

# Common error responses
class OAuth2Errors:
    UNSUPPORTED_PROVIDER = ErrorResponse(
        error_code='UNSUPPORTED_PROVIDER',
        message='OAuth provider not supported',
        status_code=404,
        suggested_action='Check the provider name and ensure it is configured'
    )
<<<<<<< HEAD
    
    INVALID_STATE = ErrorResponse(
        error_code='INVALID_OAUTH_STATE', 
=======

    INVALID_STATE = ErrorResponse(
        error_code='INVALID_OAUTH_STATE',
>>>>>>> faace65 (Add comprehensive OAuth security, testing, and coverage infrastructure)
        message='OAuth state verification failed',
        status_code=400,
        suggested_action='Please restart the OAuth flow'
    )
<<<<<<< HEAD
    
=======

>>>>>>> faace65 (Add comprehensive OAuth security, testing, and coverage infrastructure)
    MISSING_AUTH_CODE = ErrorResponse(
        error_code='MISSING_AUTH_CODE',
        message='Authorization code not provided',
        status_code=400,
        suggested_action='Please complete the OAuth authorization flow'
    )
<<<<<<< HEAD
    
=======

>>>>>>> faace65 (Add comprehensive OAuth security, testing, and coverage infrastructure)
    TOKEN_EXCHANGE_FAILED = ErrorResponse(
        error_code='TOKEN_EXCHANGE_FAILED',
        message='Failed to exchange authorization code for access token',
        status_code=502,
        suggested_action='Please try connecting your account again'
    )
<<<<<<< HEAD
    
    PROVIDER_API_ERROR = ErrorResponse(
        error_code='PROVIDER_API_ERROR', 
=======

    PROVIDER_API_ERROR = ErrorResponse(
        error_code='PROVIDER_API_ERROR',
>>>>>>> faace65 (Add comprehensive OAuth security, testing, and coverage infrastructure)
        message='Unable to communicate with OAuth provider',
        status_code=502,
        suggested_action='The service may be temporarily unavailable. Please try again later'
    )
<<<<<<< HEAD
    
=======

>>>>>>> faace65 (Add comprehensive OAuth security, testing, and coverage infrastructure)
    CONFIGURATION_ERROR = ErrorResponse(
        error_code='CONFIGURATION_ERROR',
        message='OAuth provider not properly configured',
        status_code=500,
        suggested_action='Please contact support - this is a configuration issue'
    )
```

### Updated Views with Better Error Handling
```python
def oauth2_callback(request: HttpRequest, provider: str) -> HttpResponse:
    """Finalize the Oauth2 flow with comprehensive error handling."""
<<<<<<< HEAD
    
=======

>>>>>>> faace65 (Add comprehensive OAuth security, testing, and coverage infrastructure)
    # Validate provider
    try:
        oauth2_provider = OAuth2ProviderFactory.get_provider(provider)
    except ValueError:
        error = OAuth2Errors.UNSUPPORTED_PROVIDER
        error.details = f"Provider '{provider}' is not supported"
        return error.auto_response(request)
<<<<<<< HEAD
    
    # Validate state (from previous security task)
    callback_state = request.GET.get("state")
    session_state = request.session.get(f"{provider}_oauth_state")
    
=======

    # Validate state (from previous security task)
    callback_state = request.GET.get("state")
    session_state = request.session.get(f"{provider}_oauth_state")

>>>>>>> faace65 (Add comprehensive OAuth security, testing, and coverage infrastructure)
    if not callback_state or callback_state != session_state:
        error = OAuth2Errors.INVALID_STATE
        error.details = "OAuth state parameter missing or invalid"
        return error.auto_response(request)
<<<<<<< HEAD
    
    # Clean up session state
    request.session.pop(f"{provider}_oauth_state", None)
    
=======

    # Clean up session state
    request.session.pop(f"{provider}_oauth_state", None)

>>>>>>> faace65 (Add comprehensive OAuth security, testing, and coverage infrastructure)
    # Validate authorization code
    code = request.GET.get("code")
    if not code:
        error = OAuth2Errors.MISSING_AUTH_CODE
        error.details = "OAuth provider did not return an authorization code"
        return error.auto_response(request)
<<<<<<< HEAD
    
=======

>>>>>>> faace65 (Add comprehensive OAuth security, testing, and coverage infrastructure)
    # Handle provider errors in callback
    error_param = request.GET.get("error")
    if error_param:
        error_description = request.GET.get("error_description", "No description provided")
        error = ErrorResponse(
            error_code=f"PROVIDER_ERROR_{error_param.upper()}",
            message=f"OAuth provider returned an error: {error_param}",
            details=error_description,
            status_code=400,
            suggested_action="Please try connecting your account again"
        )
        return error.auto_response(request)
<<<<<<< HEAD
    
    # Exchange code for token
    redirect_uri = request.build_absolute_uri(f"/oauth2/{provider}/callback/")
    
=======

    # Exchange code for token
    redirect_uri = request.build_absolute_uri(f"/oauth2/{provider}/callback/")

>>>>>>> faace65 (Add comprehensive OAuth security, testing, and coverage infrastructure)
    try:
        token_data = oauth2_provider.exchange_code_for_token(code, redirect_uri, request)
    except requests.RequestException as e:
        error = OAuth2Errors.PROVIDER_API_ERROR
        error.details = f"Network error: {str(e)}"
        logger.error("Provider API error for %s: %s", provider, str(e))
        return error.auto_response(request)
    except Exception as e:
        error = OAuth2Errors.CONFIGURATION_ERROR
        error.details = f"Unexpected error during token exchange: {str(e)}"
        logger.exception("Token exchange error for %s", provider)
        return error.auto_response(request)
<<<<<<< HEAD
    
=======

>>>>>>> faace65 (Add comprehensive OAuth security, testing, and coverage infrastructure)
    # Validate token response
    access_token = token_data.get("access_token")
    if not access_token:
        error = OAuth2Errors.TOKEN_EXCHANGE_FAILED
        error.details = f"Provider response: {token_data}"
        logger.error("No access token in response for %s: %s", provider, token_data)
        return error.auto_response(request)
<<<<<<< HEAD
    
=======

>>>>>>> faace65 (Add comprehensive OAuth security, testing, and coverage infrastructure)
    # Get user info
    try:
        user_info = oauth2_provider.get_user_info(access_token)
    except requests.RequestException as e:
<<<<<<< HEAD
        error = OAuth2Errors.PROVIDER_API_ERROR  
        error.details = f"Failed to fetch user information: {str(e)}"
        return error.auto_response(request)
    
=======
        error = OAuth2Errors.PROVIDER_API_ERROR
        error.details = f"Failed to fetch user information: {str(e)}"
        return error.auto_response(request)

>>>>>>> faace65 (Add comprehensive OAuth security, testing, and coverage infrastructure)
    # Save token
    try:
        oauth_token, created = OAuthToken.objects.get_or_create(
            provider=provider,
<<<<<<< HEAD
            user_id=user_info.get("id"), 
=======
            user_id=user_info.get("id"),
>>>>>>> faace65 (Add comprehensive OAuth security, testing, and coverage infrastructure)
            owner=request.user,
        )
        oauth2_provider.update_token(oauth_token, token_data, user_info)
    except Exception as e:
        error = ErrorResponse(
            error_code='TOKEN_SAVE_ERROR',
<<<<<<< HEAD
            message='Failed to save OAuth token', 
=======
            message='Failed to save OAuth token',
>>>>>>> faace65 (Add comprehensive OAuth security, testing, and coverage infrastructure)
            details=str(e),
            status_code=500,
            suggested_action='Please try connecting your account again'
        )
        logger.exception("Failed to save token for %s", provider)
        return error.auto_response(request)
<<<<<<< HEAD
    
=======

>>>>>>> faace65 (Add comprehensive OAuth security, testing, and coverage infrastructure)
    # Success response
    if request.headers.get('Accept', '').startswith('application/json'):
        return JsonResponse({
            'success': True,
            'message': f'{provider.capitalize()} account connected successfully',
            'provider': provider,
            'user_id': user_info.get('id'),
            'created': created
        })
    else:
        return HttpResponse(f"{provider.capitalize()} account connected successfully.")

def initiate_oauth2(request: HttpRequest, provider: str) -> HttpResponse:
    """Initiate OAuth2 flow with better error handling."""
<<<<<<< HEAD
    
=======

>>>>>>> faace65 (Add comprehensive OAuth security, testing, and coverage infrastructure)
    # Validate provider
    try:
        oauth2_provider = OAuth2ProviderFactory.get_provider(provider)
    except ValueError:
        error = OAuth2Errors.UNSUPPORTED_PROVIDER
        error.details = f"Provider '{provider}' is not supported or not configured"
        return error.auto_response(request)
<<<<<<< HEAD
    
=======

>>>>>>> faace65 (Add comprehensive OAuth security, testing, and coverage infrastructure)
    # Validate configuration
    try:
        state = secrets.token_urlsafe(32)
        redirect_uri = request.build_absolute_uri(f"/oauth2/{provider}/callback/")
        auth_url = oauth2_provider.get_authorization_url(state, redirect_uri, request)
    except KeyError as e:
        error = OAuth2Errors.CONFIGURATION_ERROR
        error.details = f"Missing configuration for {provider}: {str(e)}"
        logger.error("Configuration error for %s: %s", provider, str(e))
        return error.auto_response(request)
    except Exception as e:
        error = ErrorResponse(
            error_code='AUTH_URL_ERROR',
            message='Failed to generate authorization URL',
            details=str(e),
            status_code=500,
            suggested_action='Please contact support'
        )
        logger.exception("Failed to generate auth URL for %s", provider)
        return error.auto_response(request)
<<<<<<< HEAD
    
    # Store state and redirect
    request.session[f"{provider}_oauth_state"] = state
    
=======

    # Store state and redirect
    request.session[f"{provider}_oauth_state"] = state

>>>>>>> faace65 (Add comprehensive OAuth security, testing, and coverage infrastructure)
    logger.info("Initiating OAuth flow for %s user %s", provider, request.user.id)
    return redirect(auth_url)
```

### Error Template
```html
<!-- oauth2_capture/templates/oauth2_capture/error.html -->
<!DOCTYPE html>
<html>
<head>
    <title>OAuth Connection Error</title>
    <style>
        .error-container { max-width: 600px; margin: 50px auto; padding: 20px; }
        .error-code { color: #666; font-size: 0.9em; }
        .error-message { color: #c33; font-size: 1.2em; margin: 10px 0; }
        .error-details { background: #f5f5f5; padding: 15px; margin: 15px 0; }
        .suggested-action { background: #e8f4f8; padding: 15px; margin: 15px 0; }
        .back-link { margin-top: 20px; }
    </style>
</head>
<body>
    <div class="error-container">
        <h1>Connection Error</h1>
<<<<<<< HEAD
        
        <div class="error-code">Error Code: {{ error_code }}</div>
        <div class="error-message">{{ message }}</div>
        
=======

        <div class="error-code">Error Code: {{ error_code }}</div>
        <div class="error-message">{{ message }}</div>

>>>>>>> faace65 (Add comprehensive OAuth security, testing, and coverage infrastructure)
        {% if details %}
        <div class="error-details">
            <strong>Details:</strong><br>
            {{ details }}
        </div>
        {% endif %}
<<<<<<< HEAD
        
=======

>>>>>>> faace65 (Add comprehensive OAuth security, testing, and coverage infrastructure)
        {% if suggested_action %}
        <div class="suggested-action">
            <strong>What you can do:</strong><br>
            {{ suggested_action }}
        </div>
        {% endif %}
<<<<<<< HEAD
        
=======

>>>>>>> faace65 (Add comprehensive OAuth security, testing, and coverage infrastructure)
        <div class="back-link">
            <a href="/">← Back to Home</a>
        </div>
    </div>
</body>
</html>
```

## Success Criteria
- [ ] Structured error responses with specific error codes
<<<<<<< HEAD
- [ ] Appropriate HTTP status codes for different error types  
=======
- [ ] Appropriate HTTP status codes for different error types
>>>>>>> faace65 (Add comprehensive OAuth security, testing, and coverage infrastructure)
- [ ] Human-readable error messages with actionable guidance
- [ ] Support for both JSON and HTML error responses
- [ ] Comprehensive error logging for debugging
- [ ] Backward compatibility with existing error handling expectations
<<<<<<< HEAD
- [ ] Full test coverage for all error scenarios
=======
- [ ] Full test coverage for all error scenarios
>>>>>>> faace65 (Add comprehensive OAuth security, testing, and coverage infrastructure)
