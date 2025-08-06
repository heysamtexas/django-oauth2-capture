# Token Validation Helper Methods

## Objective
Create helper methods to validate OAuth tokens before making API calls. Currently, there's no way to test if a token is valid without attempting to use it, which can lead to unnecessary API failures and poor error handling.

## Context
Currently, the only token validation is checking expiration dates locally (`oauth_token.expires_at`). However, tokens can become invalid for other reasons:
- User revoked app permissions
- Provider invalidated the token
- Scope changes
- Account suspension/deletion

The library needs lightweight validation methods that can check token validity before attempting API operations.

## Technical Details

### Validation Strategies
1. **Lightweight User Info Call**: Make a minimal API call to verify token validity
<<<<<<< HEAD
2. **Token Introspection**: Use provider-specific token validation endpoints (if available)  
=======
2. **Token Introspection**: Use provider-specific token validation endpoints (if available)
>>>>>>> faace65 (Add comprehensive OAuth security, testing, and coverage infrastructure)
3. **Cached Validation**: Cache validation results to avoid excessive API calls

### Implementation Approach
Add validation methods to the `OAuth2Provider` base class and implement provider-specific validation logic.

### Core Methods Needed
- `validate_token(access_token: str) -> bool`: Simple validity check
- `validate_token_detailed(access_token: str) -> TokenValidationResult`: Detailed validation info
- `is_token_valid(oauth_token: OAuthToken) -> bool`: Convenience method for OAuthToken objects

## Testing Requirements
1. **Valid Token Test**: Verify validation passes for good tokens
<<<<<<< HEAD
2. **Invalid Token Test**: Verify validation fails for bad tokens  
=======
2. **Invalid Token Test**: Verify validation fails for bad tokens
>>>>>>> faace65 (Add comprehensive OAuth security, testing, and coverage infrastructure)
3. **Revoked Token Test**: Test validation with user-revoked permissions
4. **Network Error Test**: Handle API failures during validation
5. **Caching Test**: Verify validation results are cached appropriately
6. **Provider-Specific Test**: Test validation for each supported provider

## Dependencies
None - this is a standalone enhancement.

## Estimated Complexity
Medium (half day)

## Files to Modify
- `oauth2_capture/services/oauth2.py`: Add validation methods to base class and providers
- `oauth2_capture/models.py`: Add convenience methods to OAuthToken model
- `oauth2_capture/tests/services/test_validation.py`: Create comprehensive validation tests

## Example Code

### Base Validation Framework
```python
from dataclasses import dataclass
from enum import Enum

class TokenValidationStatus(Enum):
    VALID = "valid"
<<<<<<< HEAD
    EXPIRED = "expired" 
=======
    EXPIRED = "expired"
>>>>>>> faace65 (Add comprehensive OAuth security, testing, and coverage infrastructure)
    REVOKED = "revoked"
    INVALID = "invalid"
    UNKNOWN = "unknown"

@dataclass
class TokenValidationResult:
    status: TokenValidationStatus
    message: str
    provider: str
    user_id: str = None
    scopes: list = None
    expires_at: datetime = None
```

### OAuth2Provider Base Methods
```python
class OAuth2Provider(ABC):
<<<<<<< HEAD
    
=======

>>>>>>> faace65 (Add comprehensive OAuth security, testing, and coverage infrastructure)
    def validate_token(self, access_token: str) -> bool:
        """Quick token validation - returns True if token is valid."""
        try:
            result = self.validate_token_detailed(access_token)
            return result.status == TokenValidationStatus.VALID
        except Exception:
            logger.exception("Token validation failed for %s", self.provider_name)
            return False
<<<<<<< HEAD
    
=======

>>>>>>> faace65 (Add comprehensive OAuth security, testing, and coverage infrastructure)
    def validate_token_detailed(self, access_token: str) -> TokenValidationResult:
        """Detailed token validation with comprehensive status information."""
        try:
            user_info = self.get_user_info(access_token)
<<<<<<< HEAD
            
=======

>>>>>>> faace65 (Add comprehensive OAuth security, testing, and coverage infrastructure)
            if not user_info or "error" in user_info:
                return TokenValidationResult(
                    status=TokenValidationStatus.INVALID,
                    message=f"Token validation failed: {user_info.get('error', 'Unknown error')}",
                    provider=self.provider_name
                )
<<<<<<< HEAD
            
=======

>>>>>>> faace65 (Add comprehensive OAuth security, testing, and coverage infrastructure)
            return TokenValidationResult(
                status=TokenValidationStatus.VALID,
                message="Token is valid",
                provider=self.provider_name,
                user_id=user_info.get("id"),
                scopes=self.config.get("scope", "").split()
            )
<<<<<<< HEAD
            
=======

>>>>>>> faace65 (Add comprehensive OAuth security, testing, and coverage infrastructure)
        except requests.RequestException as e:
            if e.response and e.response.status_code == 401:
                return TokenValidationResult(
                    status=TokenValidationStatus.REVOKED,
                    message="Token has been revoked or expired",
                    provider=self.provider_name
                )
<<<<<<< HEAD
            
=======

>>>>>>> faace65 (Add comprehensive OAuth security, testing, and coverage infrastructure)
            return TokenValidationResult(
                status=TokenValidationStatus.UNKNOWN,
                message=f"Network error during validation: {str(e)}",
                provider=self.provider_name
            )
<<<<<<< HEAD
    
=======

>>>>>>> faace65 (Add comprehensive OAuth security, testing, and coverage infrastructure)
    def is_token_valid(self, oauth_token: OAuthToken) -> bool:
        """Convenience method to validate an OAuthToken object."""
        # First check local expiration
        if oauth_token.is_expired:
            return False
<<<<<<< HEAD
        
=======

>>>>>>> faace65 (Add comprehensive OAuth security, testing, and coverage infrastructure)
        # Then validate with provider
        return self.validate_token(oauth_token.access_token)
```

### OAuthToken Model Extensions
```python
class OAuthToken(models.Model):
    # ... existing fields ...
<<<<<<< HEAD
    
    last_validated_at = models.DateTimeField(
        null=True, 
        blank=True, 
        help_text="Last time this token was validated with the provider"
    )
    
=======

    last_validated_at = models.DateTimeField(
        null=True,
        blank=True,
        help_text="Last time this token was validated with the provider"
    )

>>>>>>> faace65 (Add comprehensive OAuth security, testing, and coverage infrastructure)
    validation_status = models.CharField(
        max_length=20,
        choices=[(status.value, status.value) for status in TokenValidationStatus],
        default=TokenValidationStatus.UNKNOWN.value,
        help_text="Last known validation status"
    )
<<<<<<< HEAD
    
=======

>>>>>>> faace65 (Add comprehensive OAuth security, testing, and coverage infrastructure)
    def is_validation_stale(self, max_age_minutes: int = 60) -> bool:
        """Check if validation status is stale and needs refresh."""
        if not self.last_validated_at:
            return True
<<<<<<< HEAD
        
        stale_time = timezone.now() - timedelta(minutes=max_age_minutes)
        return self.last_validated_at < stale_time
    
    def validate_with_provider(self) -> TokenValidationResult:
        """Validate this token with its provider and update status."""
        from oauth2_capture.services.oauth2 import OAuth2ProviderFactory
        
        provider = OAuth2ProviderFactory.get_provider(self.provider)
        result = provider.validate_token_detailed(self.access_token)
        
=======

        stale_time = timezone.now() - timedelta(minutes=max_age_minutes)
        return self.last_validated_at < stale_time

    def validate_with_provider(self) -> TokenValidationResult:
        """Validate this token with its provider and update status."""
        from oauth2_capture.services.oauth2 import OAuth2ProviderFactory

        provider = OAuth2ProviderFactory.get_provider(self.provider)
        result = provider.validate_token_detailed(self.access_token)

>>>>>>> faace65 (Add comprehensive OAuth security, testing, and coverage infrastructure)
        # Update validation metadata
        self.last_validated_at = timezone.now()
        self.validation_status = result.status.value
        self.save(update_fields=['last_validated_at', 'validation_status'])
<<<<<<< HEAD
        
=======

>>>>>>> faace65 (Add comprehensive OAuth security, testing, and coverage infrastructure)
        return result
```

### Usage Examples
```python
# Quick validation check
if provider.validate_token(token.access_token):
    # Proceed with API call
    pass
else:
    # Handle invalid token
    pass

# Detailed validation with specific error handling
result = provider.validate_token_detailed(token.access_token)
if result.status == TokenValidationStatus.REVOKED:
    # Redirect to re-auth
    return redirect('/oauth2/authorize/twitter')
elif result.status == TokenValidationStatus.UNKNOWN:
    # Network issue, maybe retry
    messages.warning(request, "Unable to verify token, trying anyway...")

# Model convenience method
if token.is_validation_stale():
    result = token.validate_with_provider()
    if result.status != TokenValidationStatus.VALID:
        # Handle invalid token
        pass
```

### Provider-Specific Optimizations
```python
class TwitterOAuth2Provider(OAuth2Provider):
<<<<<<< HEAD
    
=======

>>>>>>> faace65 (Add comprehensive OAuth security, testing, and coverage infrastructure)
    def validate_token_detailed(self, access_token: str) -> TokenValidationResult:
        """Twitter-specific validation using minimal user info call."""
        try:
            # Use minimal fields to reduce API usage
            headers = {"Authorization": f"Bearer {access_token}"}
            params = {"user.fields": "id"}  # Minimal fields
<<<<<<< HEAD
            
            response = requests.get(self.user_info_url, headers=headers, params=params, timeout=10)
            
=======

            response = requests.get(self.user_info_url, headers=headers, params=params, timeout=10)

>>>>>>> faace65 (Add comprehensive OAuth security, testing, and coverage infrastructure)
            if response.status_code == 200:
                data = response.json().get("data", {})
                return TokenValidationResult(
                    status=TokenValidationStatus.VALID,
                    message="Token is valid",
                    provider=self.provider_name,
                    user_id=data.get("id")
                )
            elif response.status_code == 401:
                return TokenValidationResult(
                    status=TokenValidationStatus.REVOKED,
                    message="Token has been revoked",
                    provider=self.provider_name
                )
            else:
                return TokenValidationResult(
                    status=TokenValidationStatus.INVALID,
                    message=f"Validation failed: HTTP {response.status_code}",
                    provider=self.provider_name
                )
<<<<<<< HEAD
                
=======

>>>>>>> faace65 (Add comprehensive OAuth security, testing, and coverage infrastructure)
        except requests.RequestException as e:
            return TokenValidationResult(
                status=TokenValidationStatus.UNKNOWN,
                message=f"Network error: {str(e)}",
                provider=self.provider_name
            )
```

## Success Criteria
- [ ] Lightweight token validation methods available for all providers
- [ ] Detailed validation results with specific error information
- [ ] Cached validation to prevent excessive API calls
- [ ] Model extensions for tracking validation status
- [ ] Provider-specific optimizations for minimal API usage
- [ ] Comprehensive test coverage for all validation scenarios
<<<<<<< HEAD
- [ ] Integration examples showing proper usage patterns
=======
- [ ] Integration examples showing proper usage patterns
>>>>>>> faace65 (Add comprehensive OAuth security, testing, and coverage infrastructure)
