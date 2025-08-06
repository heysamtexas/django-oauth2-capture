# Admin Interface Improvements

## Objective
Enhance the Django admin interface for the OAuthToken model to provide better visibility, management capabilities, and user experience for administrators managing OAuth tokens.

## Context
Currently, the admin interface for OAuthToken is basic and likely uses Django's default ModelAdmin. Based on the model structure, administrators need better tools to:

**Current Limitations:**
- Basic list view without useful filtering or search
- No visibility into token health (expiration, validity)
- Raw display of encrypted tokens (security/usability issue)
- No bulk operations for token management
- Limited insight into token usage patterns
- No way to test token validity from admin

**Administrator Needs:**
- Quick overview of token health across all users
- Ability to filter tokens by provider, status, expiration
- Safe display of token metadata without exposing sensitive data
- Bulk operations for expired token cleanup
- Token validation testing from admin interface
- Better user experience for token management

**Security Considerations:**
- Never display actual token values in admin
- Provide token validation without exposing tokens
- Audit logs for admin actions on tokens
- Safe token testing functionality

## Technical Details

### Admin Enhancements

1. **Enhanced List Display**
   - Token health indicators (valid, expired, expiring soon)
   - Provider icons/badges
   - User information and token age
   - Last used timestamps (if tracked)

2. **Advanced Filtering**
   - Filter by provider
   - Filter by token status (valid, expired, expiring soon)
   - Filter by user or user groups
   - Date-based filtering (created, expires, last used)

3. **Search Functionality**
   - Search by username, email
   - Search by provider
   - Search by OAuth user ID

4. **Custom Actions**
   - Bulk delete expired tokens
   - Bulk refresh tokens where possible
   - Test token validity
   - Force token refresh

5. **Enhanced Detail View**
   - Token metadata without sensitive values
   - Token validation results
   - Usage statistics (if available)
   - Related user information

6. **Security Features**
   - Masked token display (show only first/last few characters)
   - Admin action logging
   - Permission-based access to sensitive operations

## Testing Requirements
1. **Admin Interface Tests**: Test all custom admin functionality
2. **Permission Tests**: Verify admin permissions work correctly
3. **Security Tests**: Ensure tokens are not exposed in admin
4. **Bulk Action Tests**: Test bulk operations work correctly
5. **Filter/Search Tests**: Verify filtering and search functionality
6. **Custom Field Tests**: Test custom admin field displays

## Dependencies
- Token validation helpers (security task 03) for token health checking
- Token lifecycle logging (logging task 02) for usage statistics
- Token encryption (enhancement task 02) for secure token handling

## Estimated Complexity
Simple (half day)

## Files to Create/Modify
- `oauth2_capture/admin.py`: Complete admin interface implementation
- `oauth2_capture/static/oauth2_capture/admin/`: Custom admin CSS/JS
- `oauth2_capture/templates/admin/oauth2_capture/`: Custom admin templates
- `oauth2_capture/tests/test_admin.py`: Admin interface tests

## Example Implementation

### Enhanced Admin Configuration
```python
# oauth2_capture/admin.py
from django.contrib import admin
from django.contrib.auth.models import User
from django.utils.html import format_html
from django.utils.safestring import mark_safe
from django.urls import reverse, path
from django.shortcuts import get_object_or_404
from django.http import HttpResponse, JsonResponse
from django.utils import timezone
from django.db.models import Q, Count
from django.contrib import messages
from datetime import timedelta
import logging

from .models import OAuthToken
from .services.oauth2 import OAuth2ProviderFactory

logger = logging.getLogger(__name__)

class TokenHealthFilter(admin.SimpleListFilter):
    """Filter tokens by health status."""
<<<<<<< HEAD
    
    title = 'token health'
    parameter_name = 'health'
    
=======

    title = 'token health'
    parameter_name = 'health'

>>>>>>> faace65 (Add comprehensive OAuth security, testing, and coverage infrastructure)
    def lookups(self, request, model_admin):
        return (
            ('valid', 'Valid'),
            ('expired', 'Expired'),
            ('expiring_soon', 'Expiring Soon (7 days)'),
            ('no_expiry', 'No Expiry Set'),
        )
<<<<<<< HEAD
    
    def queryset(self, request, queryset):
        now = timezone.now()
        week_from_now = now + timedelta(days=7)
        
=======

    def queryset(self, request, queryset):
        now = timezone.now()
        week_from_now = now + timedelta(days=7)

>>>>>>> faace65 (Add comprehensive OAuth security, testing, and coverage infrastructure)
        if self.value() == 'valid':
            return queryset.filter(
                Q(expires_at__gt=now) | Q(expires_at__isnull=True)
            )
        elif self.value() == 'expired':
            return queryset.filter(expires_at__lt=now)
        elif self.value() == 'expiring_soon':
            return queryset.filter(
                expires_at__gt=now,
                expires_at__lte=week_from_now
            )
        elif self.value() == 'no_expiry':
            return queryset.filter(expires_at__isnull=True)
<<<<<<< HEAD
        
=======

>>>>>>> faace65 (Add comprehensive OAuth security, testing, and coverage infrastructure)
        return queryset

class ProviderFilter(admin.SimpleListFilter):
    """Filter tokens by OAuth provider."""
<<<<<<< HEAD
    
    title = 'provider'
    parameter_name = 'provider'
    
=======

    title = 'provider'
    parameter_name = 'provider'

>>>>>>> faace65 (Add comprehensive OAuth security, testing, and coverage infrastructure)
    def lookups(self, request, model_admin):
        # Get unique providers from database
        providers = OAuthToken.objects.values_list('provider', flat=True).distinct()
        return [(provider, provider.title()) for provider in providers]
<<<<<<< HEAD
    
=======

>>>>>>> faace65 (Add comprehensive OAuth security, testing, and coverage infrastructure)
    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(provider=self.value())
        return queryset

@admin.register(OAuthToken)
class OAuthTokenAdmin(admin.ModelAdmin):
    """Enhanced admin interface for OAuth tokens."""
<<<<<<< HEAD
    
=======

>>>>>>> faace65 (Add comprehensive OAuth security, testing, and coverage infrastructure)
    list_display = [
        'provider_badge',
        'user_info',
        'token_health',
        'oauth_username',
        'created_at',
        'expires_in_display',
        'actions_column'
    ]
<<<<<<< HEAD
    
=======

>>>>>>> faace65 (Add comprehensive OAuth security, testing, and coverage infrastructure)
    list_filter = [
        TokenHealthFilter,
        ProviderFilter,
        'created_at',
        'expires_at',
    ]
<<<<<<< HEAD
    
=======

>>>>>>> faace65 (Add comprehensive OAuth security, testing, and coverage infrastructure)
    search_fields = [
        'owner__username',
        'owner__email',
        'provider',
        'user_id',
        'name',
    ]
<<<<<<< HEAD
    
=======

>>>>>>> faace65 (Add comprehensive OAuth security, testing, and coverage infrastructure)
    readonly_fields = [
        'slug',
        'created_at',
        'token_health_detail',
        'masked_access_token',
        'masked_refresh_token',
        'token_info',
    ]
<<<<<<< HEAD
    
=======

>>>>>>> faace65 (Add comprehensive OAuth security, testing, and coverage infrastructure)
    fields = [
        'provider',
        'owner',
        'user_id',
        'name',
        'token_health_detail',
        'masked_access_token',
        'masked_refresh_token',
        'expires_at',
        'refresh_token_expires_at',
        'token_type',
        'scope',
        'profile_json',
        'slug',
        'created_at',
        'token_info',
    ]
<<<<<<< HEAD
    
=======

>>>>>>> faace65 (Add comprehensive OAuth security, testing, and coverage infrastructure)
    actions = [
        'delete_expired_tokens',
        'test_token_validity',
        'refresh_tokens',
    ]
<<<<<<< HEAD
    
    list_per_page = 50
    
=======

    list_per_page = 50

>>>>>>> faace65 (Add comprehensive OAuth security, testing, and coverage infrastructure)
    class Media:
        css = {
            'all': ('oauth2_capture/admin/oauth2_admin.css',)
        }
        js = ('oauth2_capture/admin/oauth2_admin.js',)
<<<<<<< HEAD
    
=======

>>>>>>> faace65 (Add comprehensive OAuth security, testing, and coverage infrastructure)
    def get_urls(self):
        """Add custom admin URLs."""
        urls = super().get_urls()
        custom_urls = [
            path(
                '<path:object_id>/test-token/',
                self.admin_site.admin_view(self.test_token_view),
                name='oauth2_capture_oauthtoken_test',
            ),
            path(
                '<path:object_id>/refresh-token/',
                self.admin_site.admin_view(self.refresh_token_view),
                name='oauth2_capture_oauthtoken_refresh',
            ),
            path(
                'health-summary/',
                self.admin_site.admin_view(self.health_summary_view),
                name='oauth2_capture_oauthtoken_health',
            ),
        ]
        return custom_urls + urls
<<<<<<< HEAD
    
=======

>>>>>>> faace65 (Add comprehensive OAuth security, testing, and coverage infrastructure)
    def provider_badge(self, obj):
        """Display provider with icon/badge."""
        provider_icons = {
            'twitter': '🐦',
            'linkedin': '💼',
            'github': '🐙',
            'google': '🔍',
            'facebook': '📘',
            'reddit': '🤖',
            'pinterest': '📌',
        }
<<<<<<< HEAD
        
        icon = provider_icons.get(obj.provider, '🔗')
        
=======

        icon = provider_icons.get(obj.provider, '🔗')

>>>>>>> faace65 (Add comprehensive OAuth security, testing, and coverage infrastructure)
        return format_html(
            '<span class="provider-badge provider-{}">{} {}</span>',
            obj.provider,
            icon,
            obj.provider.title()
        )
    provider_badge.short_description = 'Provider'
    provider_badge.admin_order_field = 'provider'
<<<<<<< HEAD
    
    def user_info(self, obj):
        """Display user information."""
        user_admin_url = reverse('admin:auth_user_change', args=[obj.owner.id])
        
=======

    def user_info(self, obj):
        """Display user information."""
        user_admin_url = reverse('admin:auth_user_change', args=[obj.owner.id])

>>>>>>> faace65 (Add comprehensive OAuth security, testing, and coverage infrastructure)
        return format_html(
            '<a href="{}">{}</a><br><small>{}</small>',
            user_admin_url,
            obj.owner.username,
            obj.owner.email
        )
    user_info.short_description = 'User'
    user_info.admin_order_field = 'owner__username'
<<<<<<< HEAD
    
=======

>>>>>>> faace65 (Add comprehensive OAuth security, testing, and coverage infrastructure)
    def token_health(self, obj):
        """Display token health status."""
        if not obj.expires_at:
            return format_html(
                '<span class="token-status no-expiry">No Expiry</span>'
            )
<<<<<<< HEAD
        
        now = timezone.now()
        
=======

        now = timezone.now()

>>>>>>> faace65 (Add comprehensive OAuth security, testing, and coverage infrastructure)
        if obj.expires_at < now:
            time_ago = now - obj.expires_at
            return format_html(
                '<span class="token-status expired">Expired<br><small>{} ago</small></span>',
                self._humanize_timedelta(time_ago)
            )
<<<<<<< HEAD
        
        time_until = obj.expires_at - now
        
=======

        time_until = obj.expires_at - now

>>>>>>> faace65 (Add comprehensive OAuth security, testing, and coverage infrastructure)
        if time_until <= timedelta(days=7):
            return format_html(
                '<span class="token-status expiring-soon">Expiring Soon<br><small>{} left</small></span>',
                self._humanize_timedelta(time_until)
            )
<<<<<<< HEAD
        
=======

>>>>>>> faace65 (Add comprehensive OAuth security, testing, and coverage infrastructure)
        return format_html(
            '<span class="token-status valid">Valid<br><small>{} left</small></span>',
            self._humanize_timedelta(time_until)
        )
    token_health.short_description = 'Health'
    token_health.admin_order_field = 'expires_at'
<<<<<<< HEAD
    
=======

>>>>>>> faace65 (Add comprehensive OAuth security, testing, and coverage infrastructure)
    def oauth_username(self, obj):
        """Display OAuth provider username."""
        username = obj.username
        if username:
            return format_html('<strong>{}</strong>', username)
        return format_html('<em>Unknown</em>')
    oauth_username.short_description = 'OAuth User'
<<<<<<< HEAD
    
=======

>>>>>>> faace65 (Add comprehensive OAuth security, testing, and coverage infrastructure)
    def expires_in_display(self, obj):
        """Display expiration in human readable format."""
        return obj.expires_in_humanized
    expires_in_display.short_description = 'Expires'
    expires_in_display.admin_order_field = 'expires_at'
<<<<<<< HEAD
    
=======

>>>>>>> faace65 (Add comprehensive OAuth security, testing, and coverage infrastructure)
    def actions_column(self, obj):
        """Display action buttons."""
        test_url = reverse('admin:oauth2_capture_oauthtoken_test', args=[obj.pk])
        refresh_url = reverse('admin:oauth2_capture_oauthtoken_refresh', args=[obj.pk])
<<<<<<< HEAD
        
        actions = [
            f'<a href="{test_url}" class="button">Test</a>',
        ]
        
        if obj.refresh_token:
            actions.append(f'<a href="{refresh_url}" class="button">Refresh</a>')
        
        return mark_safe(' '.join(actions))
    actions_column.short_description = 'Actions'
    
=======

        actions = [
            f'<a href="{test_url}" class="button">Test</a>',
        ]

        if obj.refresh_token:
            actions.append(f'<a href="{refresh_url}" class="button">Refresh</a>')

        return mark_safe(' '.join(actions))
    actions_column.short_description = 'Actions'

>>>>>>> faace65 (Add comprehensive OAuth security, testing, and coverage infrastructure)
    def token_health_detail(self, obj):
        """Detailed token health information."""
        if not obj.expires_at:
            return "No expiration set - token does not expire"
<<<<<<< HEAD
        
        now = timezone.now()
        
=======

        now = timezone.now()

>>>>>>> faace65 (Add comprehensive OAuth security, testing, and coverage infrastructure)
        if obj.expires_at < now:
            return format_html(
                '<span style="color: red;">Token expired {} ago</span>',
                self._humanize_timedelta(now - obj.expires_at)
            )
<<<<<<< HEAD
        
        time_until = obj.expires_at - now
        
=======

        time_until = obj.expires_at - now

>>>>>>> faace65 (Add comprehensive OAuth security, testing, and coverage infrastructure)
        if time_until <= timedelta(days=7):
            return format_html(
                '<span style="color: orange;">Token expires in {}</span>',
                self._humanize_timedelta(time_until)
            )
<<<<<<< HEAD
        
=======

>>>>>>> faace65 (Add comprehensive OAuth security, testing, and coverage infrastructure)
        return format_html(
            '<span style="color: green;">Token valid for {}</span>',
            self._humanize_timedelta(time_until)
        )
    token_health_detail.short_description = 'Token Health'
<<<<<<< HEAD
    
=======

>>>>>>> faace65 (Add comprehensive OAuth security, testing, and coverage infrastructure)
    def masked_access_token(self, obj):
        """Display masked access token."""
        if not obj.access_token:
            return "No access token"
<<<<<<< HEAD
        
=======

>>>>>>> faace65 (Add comprehensive OAuth security, testing, and coverage infrastructure)
        token = obj.access_token
        if len(token) > 20:
            masked = token[:8] + '...' + token[-8:]
        else:
            masked = token[:4] + '...' + token[-4:]
<<<<<<< HEAD
        
=======

>>>>>>> faace65 (Add comprehensive OAuth security, testing, and coverage infrastructure)
        return format_html(
            '<code style="background: #f0f0f0; padding: 2px 4px; border-radius: 3px;">{}</code><br>'
            '<small>Length: {} characters</small>',
            masked,
            len(token)
        )
    masked_access_token.short_description = 'Access Token (masked)'
<<<<<<< HEAD
    
=======

>>>>>>> faace65 (Add comprehensive OAuth security, testing, and coverage infrastructure)
    def masked_refresh_token(self, obj):
        """Display masked refresh token."""
        if not obj.refresh_token:
            return "No refresh token"
<<<<<<< HEAD
        
=======

>>>>>>> faace65 (Add comprehensive OAuth security, testing, and coverage infrastructure)
        token = obj.refresh_token
        if len(token) > 20:
            masked = token[:8] + '...' + token[-8:]
        else:
            masked = token[:4] + '...' + token[-4:]
<<<<<<< HEAD
        
=======

>>>>>>> faace65 (Add comprehensive OAuth security, testing, and coverage infrastructure)
        return format_html(
            '<code style="background: #f0f0f0; padding: 2px 4px; border-radius: 3px;">{}</code><br>'
            '<small>Length: {} characters</small>',
            masked,
            len(token)
        )
    masked_refresh_token.short_description = 'Refresh Token (masked)'
<<<<<<< HEAD
    
    def token_info(self, obj):
        """Display additional token information."""
        info = []
        
        if obj.token_type:
            info.append(f"Type: {obj.token_type}")
        
=======

    def token_info(self, obj):
        """Display additional token information."""
        info = []

        if obj.token_type:
            info.append(f"Type: {obj.token_type}")

>>>>>>> faace65 (Add comprehensive OAuth security, testing, and coverage infrastructure)
        if obj.scope:
            scopes = obj.scope.split()
            if len(scopes) > 5:
                scope_display = ', '.join(scopes[:5]) + f' ... (+{len(scopes)-5} more)'
            else:
                scope_display = ', '.join(scopes)
            info.append(f"Scopes: {scope_display}")
<<<<<<< HEAD
        
=======

>>>>>>> faace65 (Add comprehensive OAuth security, testing, and coverage infrastructure)
        if obj.profile_json:
            profile_keys = list(obj.profile_json.keys())
            if profile_keys:
                info.append(f"Profile data: {', '.join(profile_keys[:10])}")
<<<<<<< HEAD
        
        return format_html('<br>'.join(info)) if info else "No additional information"
    token_info.short_description = 'Token Information'
    
=======

        return format_html('<br>'.join(info)) if info else "No additional information"
    token_info.short_description = 'Token Information'

>>>>>>> faace65 (Add comprehensive OAuth security, testing, and coverage infrastructure)
    def delete_expired_tokens(self, request, queryset):
        """Delete expired tokens."""
        expired_tokens = queryset.filter(expires_at__lt=timezone.now())
        count = expired_tokens.count()
<<<<<<< HEAD
        
=======

>>>>>>> faace65 (Add comprehensive OAuth security, testing, and coverage infrastructure)
        if count > 0:
            expired_tokens.delete()
            self.message_user(
                request,
                f"Successfully deleted {count} expired tokens.",
                messages.SUCCESS
            )
        else:
            self.message_user(
                request,
                "No expired tokens found in selection.",
                messages.INFO
            )
    delete_expired_tokens.short_description = "Delete expired tokens"
<<<<<<< HEAD
    
    def test_token_validity(self, request, queryset):
        """Test token validity for selected tokens."""
        results = {'valid': 0, 'invalid': 0, 'error': 0}
        
=======

    def test_token_validity(self, request, queryset):
        """Test token validity for selected tokens."""
        results = {'valid': 0, 'invalid': 0, 'error': 0}

>>>>>>> faace65 (Add comprehensive OAuth security, testing, and coverage infrastructure)
        for token in queryset:
            try:
                provider = OAuth2ProviderFactory.get_provider(token.provider)
                access_token = provider.get_valid_token(token)
<<<<<<< HEAD
                
=======

>>>>>>> faace65 (Add comprehensive OAuth security, testing, and coverage infrastructure)
                if access_token:
                    results['valid'] += 1
                else:
                    results['invalid'] += 1
<<<<<<< HEAD
                    
            except Exception as e:
                results['error'] += 1
                logger.exception(f"Error testing token {token.id}: {str(e)}")
        
=======

            except Exception as e:
                results['error'] += 1
                logger.exception(f"Error testing token {token.id}: {str(e)}")

>>>>>>> faace65 (Add comprehensive OAuth security, testing, and coverage infrastructure)
        self.message_user(
            request,
            f"Token validation results: {results['valid']} valid, "
            f"{results['invalid']} invalid, {results['error']} errors",
            messages.INFO
        )
    test_token_validity.short_description = "Test token validity"
<<<<<<< HEAD
    
    def refresh_tokens(self, request, queryset):
        """Attempt to refresh selected tokens."""
        results = {'refreshed': 0, 'failed': 0, 'no_refresh_token': 0}
        
=======

    def refresh_tokens(self, request, queryset):
        """Attempt to refresh selected tokens."""
        results = {'refreshed': 0, 'failed': 0, 'no_refresh_token': 0}

>>>>>>> faace65 (Add comprehensive OAuth security, testing, and coverage infrastructure)
        for token in queryset:
            if not token.refresh_token:
                results['no_refresh_token'] += 1
                continue
<<<<<<< HEAD
            
            try:
                provider = OAuth2ProviderFactory.get_provider(token.provider)
                access_token = provider.get_valid_token(token)
                
=======

            try:
                provider = OAuth2ProviderFactory.get_provider(token.provider)
                access_token = provider.get_valid_token(token)

>>>>>>> faace65 (Add comprehensive OAuth security, testing, and coverage infrastructure)
                if access_token:
                    results['refreshed'] += 1
                else:
                    results['failed'] += 1
<<<<<<< HEAD
                    
            except Exception as e:
                results['failed'] += 1
                logger.exception(f"Error refreshing token {token.id}: {str(e)}")
        
=======

            except Exception as e:
                results['failed'] += 1
                logger.exception(f"Error refreshing token {token.id}: {str(e)}")

>>>>>>> faace65 (Add comprehensive OAuth security, testing, and coverage infrastructure)
        self.message_user(
            request,
            f"Refresh results: {results['refreshed']} refreshed, "
            f"{results['failed']} failed, {results['no_refresh_token']} no refresh token",
            messages.INFO
        )
    refresh_tokens.short_description = "Refresh tokens"
<<<<<<< HEAD
    
    def test_token_view(self, request, object_id):
        """Test a single token's validity."""
        token = get_object_or_404(OAuthToken, pk=object_id)
        
        try:
            provider = OAuth2ProviderFactory.get_provider(token.provider)
            
            # Test token validity
            access_token = provider.get_valid_token(token)
            
            if access_token:
                # Try to get user info to fully test token
                user_info = provider.get_user_info(access_token)
                
=======

    def test_token_view(self, request, object_id):
        """Test a single token's validity."""
        token = get_object_or_404(OAuthToken, pk=object_id)

        try:
            provider = OAuth2ProviderFactory.get_provider(token.provider)

            # Test token validity
            access_token = provider.get_valid_token(token)

            if access_token:
                # Try to get user info to fully test token
                user_info = provider.get_user_info(access_token)

>>>>>>> faace65 (Add comprehensive OAuth security, testing, and coverage infrastructure)
                result = {
                    'valid': True,
                    'message': 'Token is valid and working',
                    'user_info': {
                        'id': user_info.get('id'),
                        'name': user_info.get('name'),
                        'username': user_info.get('username', user_info.get('login')),
                        'email': user_info.get('email')
                    }
                }
            else:
                result = {
                    'valid': False,
                    'message': 'Token is invalid or expired'
                }
<<<<<<< HEAD
                
=======

>>>>>>> faace65 (Add comprehensive OAuth security, testing, and coverage infrastructure)
        except Exception as e:
            result = {
                'valid': False,
                'message': f'Error testing token: {str(e)}'
            }
<<<<<<< HEAD
        
        return JsonResponse(result)
    
    def refresh_token_view(self, request, object_id):
        """Refresh a single token."""
        token = get_object_or_404(OAuthToken, pk=object_id)
        
=======

        return JsonResponse(result)

    def refresh_token_view(self, request, object_id):
        """Refresh a single token."""
        token = get_object_or_404(OAuthToken, pk=object_id)

>>>>>>> faace65 (Add comprehensive OAuth security, testing, and coverage infrastructure)
        if not token.refresh_token:
            return JsonResponse({
                'success': False,
                'message': 'No refresh token available'
            })
<<<<<<< HEAD
        
        try:
            provider = OAuth2ProviderFactory.get_provider(token.provider)
            
            # Force refresh by temporarily setting token as expired
            original_expires_at = token.expires_at
            token.expires_at = timezone.now() - timedelta(hours=1)
            
            # Get valid token (will trigger refresh)
            access_token = provider.get_valid_token(token)
            
=======

        try:
            provider = OAuth2ProviderFactory.get_provider(token.provider)

            # Force refresh by temporarily setting token as expired
            original_expires_at = token.expires_at
            token.expires_at = timezone.now() - timedelta(hours=1)

            # Get valid token (will trigger refresh)
            access_token = provider.get_valid_token(token)

>>>>>>> faace65 (Add comprehensive OAuth security, testing, and coverage infrastructure)
            if access_token:
                result = {
                    'success': True,
                    'message': 'Token refreshed successfully',
                    'new_expires_at': token.expires_at.isoformat() if token.expires_at else None
                }
            else:
                # Restore original expiration if refresh failed
                token.expires_at = original_expires_at
                token.save()
<<<<<<< HEAD
                
=======

>>>>>>> faace65 (Add comprehensive OAuth security, testing, and coverage infrastructure)
                result = {
                    'success': False,
                    'message': 'Token refresh failed'
                }
<<<<<<< HEAD
                
=======

>>>>>>> faace65 (Add comprehensive OAuth security, testing, and coverage infrastructure)
        except Exception as e:
            result = {
                'success': False,
                'message': f'Error refreshing token: {str(e)}'
            }
<<<<<<< HEAD
        
        return JsonResponse(result)
    
=======

        return JsonResponse(result)

>>>>>>> faace65 (Add comprehensive OAuth security, testing, and coverage infrastructure)
    def health_summary_view(self, request):
        """Display token health summary."""
        now = timezone.now()
        week_from_now = now + timedelta(days=7)
<<<<<<< HEAD
        
=======

>>>>>>> faace65 (Add comprehensive OAuth security, testing, and coverage infrastructure)
        summary = {
            'total_tokens': OAuthToken.objects.count(),
            'valid_tokens': OAuthToken.objects.filter(
                Q(expires_at__gt=now) | Q(expires_at__isnull=True)
            ).count(),
            'expired_tokens': OAuthToken.objects.filter(expires_at__lt=now).count(),
            'expiring_soon': OAuthToken.objects.filter(
                expires_at__gt=now, expires_at__lte=week_from_now
            ).count(),
            'by_provider': list(
                OAuthToken.objects.values('provider')
                .annotate(count=Count('id'))
                .order_by('-count')
            )
        }
<<<<<<< HEAD
        
        return JsonResponse(summary)
    
=======

        return JsonResponse(summary)

>>>>>>> faace65 (Add comprehensive OAuth security, testing, and coverage infrastructure)
    def _humanize_timedelta(self, td):
        """Convert timedelta to human readable string."""
        days = td.days
        hours, remainder = divmod(td.seconds, 3600)
        minutes, _ = divmod(remainder, 60)
<<<<<<< HEAD
        
=======

>>>>>>> faace65 (Add comprehensive OAuth security, testing, and coverage infrastructure)
        if days > 0:
            return f"{days}d {hours}h"
        elif hours > 0:
            return f"{hours}h {minutes}m"
        else:
            return f"{minutes}m"

# Custom admin site configuration
admin.site.site_header = "OAuth2 Capture Administration"
admin.site.site_title = "OAuth2 Capture Admin"
admin.site.index_title = "Welcome to OAuth2 Capture Administration"
```

### Custom Admin Styles
```css
/* oauth2_capture/static/oauth2_capture/admin/oauth2_admin.css */

.provider-badge {
    display: inline-block;
    padding: 2px 8px;
    border-radius: 12px;
    font-size: 11px;
    font-weight: bold;
    color: white;
    text-transform: uppercase;
}

.provider-twitter { background-color: #1da1f2; }
.provider-linkedin { background-color: #0077b5; }
.provider-github { background-color: #333; }
.provider-google { background-color: #4285f4; }
.provider-facebook { background-color: #1877f2; }
.provider-reddit { background-color: #ff4500; }
.provider-pinterest { background-color: #e60023; }

.token-status {
    display: inline-block;
    padding: 4px 8px;
    border-radius: 4px;
    font-size: 11px;
    font-weight: bold;
    text-align: center;
    min-width: 60px;
}

.token-status.valid {
    background-color: #d4edda;
    color: #155724;
    border: 1px solid #c3e6cb;
}

.token-status.expired {
    background-color: #f8d7da;
    color: #721c24;
    border: 1px solid #f5c6cb;
}

.token-status.expiring-soon {
    background-color: #fff3cd;
    color: #856404;
    border: 1px solid #ffeaa7;
}

.token-status.no-expiry {
    background-color: #e2e3e5;
    color: #383d41;
    border: 1px solid #d6d8db;
}

/* Responsive improvements */
@media (max-width: 768px) {
    .provider-badge, .token-status {
        font-size: 10px;
        padding: 2px 4px;
    }
}

/* Action buttons */
.button {
    background-color: #417690;
    color: white;
    border: none;
    padding: 2px 8px;
    border-radius: 3px;
    text-decoration: none;
    font-size: 11px;
    margin-right: 4px;
}

.button:hover {
    background-color: #205067;
    color: white;
    text-decoration: none;
}

/* Admin form improvements */
.form-row .token-status {
    margin-top: 4px;
}

/* Health summary dashboard styles */
.health-summary {
    background: white;
    padding: 20px;
    border: 1px solid #ddd;
    border-radius: 4px;
    margin: 20px 0;
}

.health-summary h3 {
    margin-top: 0;
    color: #333;
}

.health-stats {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
    gap: 20px;
    margin: 20px 0;
}

.health-stat {
    text-align: center;
    padding: 15px;
    border: 1px solid #ddd;
    border-radius: 4px;
}

.health-stat .number {
    font-size: 2em;
    font-weight: bold;
    color: #417690;
}

.health-stat .label {
    color: #666;
    font-size: 0.9em;
}
```

### Custom Admin JavaScript
```javascript
// oauth2_capture/static/oauth2_capture/admin/oauth2_admin.js

(function($) {
    'use strict';
<<<<<<< HEAD
    
=======

>>>>>>> faace65 (Add comprehensive OAuth security, testing, and coverage infrastructure)
    // Test token functionality
    function testToken(url) {
        $.get(url)
            .done(function(data) {
                if (data.valid) {
                    alert('Token is valid!\n\n' + data.message);
                } else {
                    alert('Token is invalid!\n\n' + data.message);
                }
            })
            .fail(function() {
                alert('Error testing token. Please check the logs.');
            });
    }
<<<<<<< HEAD
    
=======

>>>>>>> faace65 (Add comprehensive OAuth security, testing, and coverage infrastructure)
    // Refresh token functionality
    function refreshToken(url) {
        if (!confirm('Are you sure you want to refresh this token?')) {
            return;
        }
<<<<<<< HEAD
        
=======

>>>>>>> faace65 (Add comprehensive OAuth security, testing, and coverage infrastructure)
        $.get(url)
            .done(function(data) {
                if (data.success) {
                    alert('Token refreshed successfully!\n\n' + data.message);
                    location.reload(); // Refresh page to show updated data
                } else {
                    alert('Token refresh failed!\n\n' + data.message);
                }
            })
            .fail(function() {
                alert('Error refreshing token. Please check the logs.');
            });
    }
<<<<<<< HEAD
    
=======

>>>>>>> faace65 (Add comprehensive OAuth security, testing, and coverage infrastructure)
    // Bind click events to action buttons
    $(document).ready(function() {
        // Test token buttons
        $('.test-token-btn').click(function(e) {
            e.preventDefault();
            testToken($(this).attr('href'));
        });
<<<<<<< HEAD
        
=======

>>>>>>> faace65 (Add comprehensive OAuth security, testing, and coverage infrastructure)
        // Refresh token buttons
        $('.refresh-token-btn').click(function(e) {
            e.preventDefault();
            refreshToken($(this).attr('href'));
        });
<<<<<<< HEAD
        
=======

>>>>>>> faace65 (Add comprehensive OAuth security, testing, and coverage infrastructure)
        // Add CSS classes to action buttons
        $('a[href*="/test-token/"]').addClass('button test-token-btn');
        $('a[href*="/refresh-token/"]').addClass('button refresh-token-btn');
    });
<<<<<<< HEAD
    
=======

>>>>>>> faace65 (Add comprehensive OAuth security, testing, and coverage infrastructure)
})(django.jQuery);
```

### Admin Templates
```html
<!-- oauth2_capture/templates/admin/oauth2_capture/oauthtoken/change_list.html -->
{% extends "admin/change_list.html" %}
{% load static %}

{% block content_title %}
    <h1>OAuth Tokens</h1>
    <div class="health-summary">
        <h3>Token Health Overview</h3>
        <div id="health-stats" class="health-stats">
            <div class="health-stat">
                <div class="number" id="total-tokens">-</div>
                <div class="label">Total Tokens</div>
            </div>
            <div class="health-stat">
                <div class="number" id="valid-tokens">-</div>
                <div class="label">Valid Tokens</div>
            </div>
            <div class="health-stat">
                <div class="number" id="expired-tokens">-</div>
                <div class="label">Expired Tokens</div>
            </div>
            <div class="health-stat">
                <div class="number" id="expiring-soon">-</div>
                <div class="label">Expiring Soon</div>
            </div>
        </div>
    </div>
{% endblock %}

{% block extrahead %}
    {{ block.super }}
    <script>
        // Load health summary
        fetch('{% url "admin:oauth2_capture_oauthtoken_health" %}')
            .then(response => response.json())
            .then(data => {
                document.getElementById('total-tokens').textContent = data.total_tokens;
                document.getElementById('valid-tokens').textContent = data.valid_tokens;
                document.getElementById('expired-tokens').textContent = data.expired_tokens;
                document.getElementById('expiring-soon').textContent = data.expiring_soon;
            })
            .catch(error => console.error('Error loading health summary:', error));
    </script>
{% endblock %}
```

### Admin Tests
```python
# oauth2_capture/tests/test_admin.py
from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils import timezone
from datetime import timedelta

from oauth2_capture.models import OAuthToken
from oauth2_capture.admin import OAuthTokenAdmin
from .fixtures import OAuthTestData

class OAuthTokenAdminTests(TestCase):
<<<<<<< HEAD
    
    def setUp(self):
        self.client = Client()
        
=======

    def setUp(self):
        self.client = Client()

>>>>>>> faace65 (Add comprehensive OAuth security, testing, and coverage infrastructure)
        # Create admin user
        self.admin_user = User.objects.create_user(
            username='admin',
            email='admin@example.com',
            password='adminpass',
            is_staff=True,
            is_superuser=True
        )
<<<<<<< HEAD
        
        # Create regular user for tokens
        self.user = OAuthTestData.create_test_user()
        
        # Create test tokens
        self.valid_token = OAuthTestData.create_test_token(
            self.user, 
            provider='twitter',
            expired=False
        )
        
        self.expired_token = OAuthTestData.create_test_token(
            self.user,
            provider='github', 
            expired=True
        )
        
        self.client.login(username='admin', password='adminpass')
    
=======

        # Create regular user for tokens
        self.user = OAuthTestData.create_test_user()

        # Create test tokens
        self.valid_token = OAuthTestData.create_test_token(
            self.user,
            provider='twitter',
            expired=False
        )

        self.expired_token = OAuthTestData.create_test_token(
            self.user,
            provider='github',
            expired=True
        )

        self.client.login(username='admin', password='adminpass')

>>>>>>> faace65 (Add comprehensive OAuth security, testing, and coverage infrastructure)
    def test_admin_list_view(self):
        """Test admin list view displays tokens correctly."""
        url = reverse('admin:oauth2_capture_oauthtoken_changelist')
        response = self.client.get(url)
<<<<<<< HEAD
        
=======

>>>>>>> faace65 (Add comprehensive OAuth security, testing, and coverage infrastructure)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'twitter')
        self.assertContains(response, 'github')
        self.assertContains(response, self.user.username)
<<<<<<< HEAD
    
    def test_admin_filters(self):
        """Test admin filters work correctly."""
        url = reverse('admin:oauth2_capture_oauthtoken_changelist')
        
=======

    def test_admin_filters(self):
        """Test admin filters work correctly."""
        url = reverse('admin:oauth2_capture_oauthtoken_changelist')

>>>>>>> faace65 (Add comprehensive OAuth security, testing, and coverage infrastructure)
        # Test provider filter
        response = self.client.get(url, {'provider': 'twitter'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'twitter')
<<<<<<< HEAD
        
=======

>>>>>>> faace65 (Add comprehensive OAuth security, testing, and coverage infrastructure)
        # Test health filter
        response = self.client.get(url, {'health': 'expired'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'github')  # Our expired token
<<<<<<< HEAD
    
    def test_admin_search(self):
        """Test admin search functionality."""
        url = reverse('admin:oauth2_capture_oauthtoken_changelist')
        
=======

    def test_admin_search(self):
        """Test admin search functionality."""
        url = reverse('admin:oauth2_capture_oauthtoken_changelist')

>>>>>>> faace65 (Add comprehensive OAuth security, testing, and coverage infrastructure)
        # Search by username
        response = self.client.get(url, {'q': self.user.username})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.user.username)
<<<<<<< HEAD
        
=======

>>>>>>> faace65 (Add comprehensive OAuth security, testing, and coverage infrastructure)
        # Search by provider
        response = self.client.get(url, {'q': 'twitter'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'twitter')
<<<<<<< HEAD
    
=======

>>>>>>> faace65 (Add comprehensive OAuth security, testing, and coverage infrastructure)
    def test_token_detail_view(self):
        """Test admin detail view shows masked tokens."""
        url = reverse('admin:oauth2_capture_oauthtoken_change', args=[self.valid_token.pk])
        response = self.client.get(url)
<<<<<<< HEAD
        
        self.assertEqual(response.status_code, 200)
        
        # Should show masked token, not full token
        self.assertNotContains(response, self.valid_token.access_token)
        self.assertContains(response, '...')  # Masked indicator
    
    def test_bulk_delete_expired_action(self):
        """Test bulk delete expired tokens action."""
        url = reverse('admin:oauth2_capture_oauthtoken_changelist')
        
=======

        self.assertEqual(response.status_code, 200)

        # Should show masked token, not full token
        self.assertNotContains(response, self.valid_token.access_token)
        self.assertContains(response, '...')  # Masked indicator

    def test_bulk_delete_expired_action(self):
        """Test bulk delete expired tokens action."""
        url = reverse('admin:oauth2_capture_oauthtoken_changelist')

>>>>>>> faace65 (Add comprehensive OAuth security, testing, and coverage infrastructure)
        # Post action
        response = self.client.post(url, {
            'action': 'delete_expired_tokens',
            '_selected_action': [self.valid_token.pk, self.expired_token.pk]
        })
<<<<<<< HEAD
        
        self.assertEqual(response.status_code, 302)  # Redirect after action
        
        # Check that expired token was deleted
        self.assertTrue(OAuthToken.objects.filter(pk=self.valid_token.pk).exists())
        self.assertFalse(OAuthToken.objects.filter(pk=self.expired_token.pk).exists())
    
=======

        self.assertEqual(response.status_code, 302)  # Redirect after action

        # Check that expired token was deleted
        self.assertTrue(OAuthToken.objects.filter(pk=self.valid_token.pk).exists())
        self.assertFalse(OAuthToken.objects.filter(pk=self.expired_token.pk).exists())

>>>>>>> faace65 (Add comprehensive OAuth security, testing, and coverage infrastructure)
    def test_health_summary_view(self):
        """Test health summary API endpoint."""
        url = reverse('admin:oauth2_capture_oauthtoken_health')
        response = self.client.get(url)
<<<<<<< HEAD
        
        self.assertEqual(response.status_code, 200)
        
=======

        self.assertEqual(response.status_code, 200)

>>>>>>> faace65 (Add comprehensive OAuth security, testing, and coverage infrastructure)
        data = response.json()
        self.assertIn('total_tokens', data)
        self.assertIn('valid_tokens', data)
        self.assertIn('expired_tokens', data)
        self.assertIn('by_provider', data)
<<<<<<< HEAD
        
        self.assertEqual(data['total_tokens'], 2)
        self.assertEqual(data['expired_tokens'], 1)
    
=======

        self.assertEqual(data['total_tokens'], 2)
        self.assertEqual(data['expired_tokens'], 1)

>>>>>>> faace65 (Add comprehensive OAuth security, testing, and coverage infrastructure)
    def test_admin_permissions(self):
        """Test admin permissions are enforced."""
        # Create non-staff user
        regular_user = User.objects.create_user(
            username='regular',
            password='regularpass'
        )
<<<<<<< HEAD
        
        client = Client()
        client.login(username='regular', password='regularpass')
        
        url = reverse('admin:oauth2_capture_oauthtoken_changelist')
        response = client.get(url)
        
        # Should redirect to login
        self.assertEqual(response.status_code, 302)
    
    def test_masked_token_display(self):
        """Test that tokens are properly masked in admin."""
        admin = OAuthTokenAdmin(OAuthToken, None)
        
=======

        client = Client()
        client.login(username='regular', password='regularpass')

        url = reverse('admin:oauth2_capture_oauthtoken_changelist')
        response = client.get(url)

        # Should redirect to login
        self.assertEqual(response.status_code, 302)

    def test_masked_token_display(self):
        """Test that tokens are properly masked in admin."""
        admin = OAuthTokenAdmin(OAuthToken, None)

>>>>>>> faace65 (Add comprehensive OAuth security, testing, and coverage infrastructure)
        # Test masked access token
        masked = admin.masked_access_token(self.valid_token)
        self.assertIn('...', masked)
        self.assertNotIn(self.valid_token.access_token, masked)
<<<<<<< HEAD
        
=======

>>>>>>> faace65 (Add comprehensive OAuth security, testing, and coverage infrastructure)
        # Test masked refresh token
        masked = admin.masked_refresh_token(self.valid_token)
        self.assertIn('...', masked)
        self.assertNotIn(self.valid_token.refresh_token, masked)
<<<<<<< HEAD
    
    def test_token_health_display(self):
        """Test token health display method."""
        admin = OAuthTokenAdmin(OAuthToken, None)
        
        # Valid token
        health = admin.token_health(self.valid_token)
        self.assertIn('Valid', health)
        
        # Expired token
        health = admin.token_health(self.expired_token)
        self.assertIn('Expired', health)
        
=======

    def test_token_health_display(self):
        """Test token health display method."""
        admin = OAuthTokenAdmin(OAuthToken, None)

        # Valid token
        health = admin.token_health(self.valid_token)
        self.assertIn('Valid', health)

        # Expired token
        health = admin.token_health(self.expired_token)
        self.assertIn('Expired', health)

>>>>>>> faace65 (Add comprehensive OAuth security, testing, and coverage infrastructure)
        # Token with no expiry
        no_expiry_token = OAuthToken.objects.create(
            provider='test',
            user_id='123',
            access_token='test_token',
            owner=self.user,
            expires_at=None
        )
<<<<<<< HEAD
        
=======

>>>>>>> faace65 (Add comprehensive OAuth security, testing, and coverage infrastructure)
        health = admin.token_health(no_expiry_token)
        self.assertIn('No Expiry', health)
```

## Success Criteria
- [ ] Enhanced admin interface with health indicators and provider badges
- [ ] Comprehensive filtering and search functionality
- [ ] Secure token display with masking of sensitive values
- [ ] Bulk operations for token management
- [ ] Token testing and refresh functionality from admin
- [ ] Health summary dashboard for token overview
- [ ] Custom styling for improved user experience
- [ ] Full test coverage of admin functionality
<<<<<<< HEAD
- [ ] Proper permission handling and security measures
=======
- [ ] Proper permission handling and security measures
>>>>>>> faace65 (Add comprehensive OAuth security, testing, and coverage infrastructure)
