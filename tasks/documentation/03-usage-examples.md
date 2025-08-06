# Usage Examples and Best Practices Documentation

## Objective
Create comprehensive usage examples and best practices documentation that demonstrates real-world implementation patterns, common use cases, and production-ready code for the oauth2_capture library.

## Context
Currently, the README.md provides basic usage examples, but lacks:

**Missing Usage Documentation:**
- Complete end-to-end implementation examples
- Production-ready code patterns
- Error handling best practices
- Performance optimization techniques
- Security considerations
- Advanced use cases and patterns

**Current README Examples:**
- Basic OAuth flow setup (lines 156-193)
- Simple token retrieval example
- Basic provider extension example (lines 197-228)

**Real-World Gaps:**
- No complete Django app examples
- Limited error handling patterns
- No production deployment examples
- Missing performance and security guidance
- No testing examples for integrations

## Technical Details

### Documentation Categories

1. **Getting Started Examples**
   - Django project integration
   - Basic OAuth flow implementation
   - First API call examples

2. **Common Use Cases**
   - Social media posting applications
   - Content aggregation systems
   - Multi-provider authentication
   - Background task integration

3. **Advanced Patterns**
   - Custom provider implementation
   - Token management strategies
   - Error handling and recovery
   - Performance optimization

4. **Production Examples**
   - Security hardening
   - Monitoring and logging
   - Deployment configurations
   - Scaling considerations

5. **Testing and Development**
   - Unit testing OAuth flows
   - Mocking provider responses
   - Development environment setup
   - Debugging techniques

### Code Quality Standards
- **Complete examples**: Full working code, not snippets
- **Error handling**: Comprehensive error scenarios
- **Documentation**: Inline comments explaining design decisions
- **Security**: Demonstrate secure practices
- **Performance**: Show optimization techniques

## Testing Requirements
1. **Code Validation**: All examples must be tested and working
2. **Django Integration**: Examples work with current Django versions
3. **Provider Compatibility**: Examples work with all supported providers
4. **Error Scenario Coverage**: Examples handle common failure cases
5. **Documentation Clarity**: Non-technical users can follow examples

## Dependencies
- Working oauth2_capture library installation
- Test Django project for validating examples
- Provider credentials for testing examples
- Integration with other task documentation (security, testing, logging)

## Estimated Complexity
Medium (1 day)

## Files to Create
- `docs/usage-examples.md`: Main usage examples documentation
- `examples/basic-social-app/`: Complete Django app example
- `examples/multi-provider-dashboard/`: Advanced multi-provider example
- `examples/background-tasks/`: Background job integration example
- `examples/testing-patterns/`: Testing examples and patterns
- `docs/production-guide.md`: Production deployment and security guide

## Example Documentation

### Main Usage Examples Documentation
```markdown
# docs/usage-examples.md

# Usage Examples and Best Practices

This guide provides comprehensive examples of using oauth2_capture in real-world Django applications, from basic setup to advanced production patterns.

## Table of Contents

1. [Quick Start](#quick-start)
2. [Basic Social Media App](#basic-social-media-app)
3. [Multi-Provider Dashboard](#multi-provider-dashboard)
4. [Background Task Integration](#background-task-integration)
5. [Custom Provider Implementation](#custom-provider-implementation)
6. [Error Handling Patterns](#error-handling-patterns)
7. [Testing Your Integration](#testing-your-integration)
8. [Production Best Practices](#production-best-practices)

## Quick Start

### 1. Installation and Setup

```bash
# Install the package
pip install oauth2_capture

# Or for development
pip install -e .
```

### 2. Django Configuration

```python
# settings.py
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'oauth2_capture',  # Add this
    'myapp',
]

# OAuth2 provider configuration
OAUTH2_CONFIG = {
    "twitter": {
        "client_id": os.environ["TWITTER_CLIENT_ID"],
        "client_secret": os.environ["TWITTER_CLIENT_SECRET"],
        "scope": "tweet.read users.read tweet.write offline.access",
        "code_verifier": "challenge",
    },
    "github": {
        "client_id": os.environ["GITHUB_CLIENT_ID"],
        "client_secret": os.environ["GITHUB_CLIENT_SECRET"],
        "scope": "user repo",
    },
}
```

### 3. URL Configuration

```python
# urls.py
from django.urls import include, path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('oauth2/', include('oauth2_capture.urls')),
    path('', include('myapp.urls')),
]
```

### 4. Basic Template

```html
<!-- templates/connect.html -->
<h2>Connect Your Accounts</h2>

<div class="oauth-connections">
    <a href="{% url 'oauth2_capture:authorize' 'twitter' %}" class="btn btn-primary">
        Connect Twitter
    </a>
    <a href="{% url 'oauth2_capture:authorize' 'github' %}" class="btn btn-dark">
        Connect GitHub
    </a>
</div>
```

## Basic Social Media App

Here's a complete example of a simple social media posting application:

### Models and Views

```python
# myapp/models.py
from django.db import models
from django.contrib.auth.models import User

class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField(max_length=280)
    providers = models.JSONField(default=list)  # ['twitter', 'linkedin']
    created_at = models.DateTimeField(auto_now_add=True)
    posted_at = models.DateTimeField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=[
        ('draft', 'Draft'),
        ('posting', 'Posting'),
        ('posted', 'Posted'),
        ('failed', 'Failed')
    ], default='draft')
    error_message = models.TextField(blank=True)

    class Meta:
        ordering = ['-created_at']

class PostResult(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='results')
    provider = models.CharField(max_length=50)
    success = models.BooleanField()
    external_id = models.CharField(max_length=100, blank=True)
    external_url = models.URLField(blank=True)
    error_message = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
```

```python
# myapp/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from django.http import JsonResponse
import json

from oauth2_capture.models import OAuthToken
from oauth2_capture.services.oauth2 import OAuth2ProviderFactory
from .models import Post, PostResult

@login_required
def dashboard(request):
    """Main dashboard showing user's posts and connected accounts."""
    
    # Get user's connected accounts
    connected_accounts = {}
    tokens = OAuthToken.objects.filter(owner=request.user)
    
    for token in tokens:
        try:
            provider = OAuth2ProviderFactory.get_provider(token.provider)
            access_token = provider.get_valid_token(token)
            connected_accounts[token.provider] = {
                'connected': access_token is not None,
                'username': token.username,
                'reauth_url': f'/oauth2/{token.provider}/authorize/' if not access_token else None
            }
        except Exception as e:
            connected_accounts[token.provider] = {
                'connected': False,
                'error': str(e),
                'reauth_url': f'/oauth2/{token.provider}/authorize/'
            }
    
    # Get user's recent posts
    posts = Post.objects.filter(user=request.user)[:10]
    
    context = {
        'connected_accounts': connected_accounts,
        'posts': posts,
        'available_providers': ['twitter', 'linkedin', 'github']
    }
    
    return render(request, 'myapp/dashboard.html', context)

@login_required
def create_post(request):
    """Create a new post."""
    if request.method == 'POST':
        content = request.POST.get('content', '').strip()
        selected_providers = request.POST.getlist('providers')
        
        if not content:
            messages.error(request, 'Post content cannot be empty')
            return redirect('dashboard')
        
        if not selected_providers:
            messages.error(request, 'Please select at least one provider')
            return redirect('dashboard')
        
        # Create the post
        post = Post.objects.create(
            user=request.user,
            content=content,
            providers=selected_providers,
            status='draft'
        )
        
        # Attempt to post immediately
        success = post_to_providers(post)
        
        if success:
            messages.success(request, 'Post created successfully!')
        else:
            messages.warning(request, 'Post created but some providers failed. Check post details.')
        
        return redirect('post_detail', post_id=post.id)
    
    return redirect('dashboard')

def post_to_providers(post):
    """Post content to all selected providers."""
    post.status = 'posting'
    post.save()
    
    all_success = True
    
    for provider_name in post.providers:
        try:
            result = post_to_single_provider(post, provider_name)
            
            PostResult.objects.create(
                post=post,
                provider=provider_name,
                success=result['success'],
                external_id=result.get('external_id', ''),
                external_url=result.get('external_url', ''),
                error_message=result.get('error_message', '')
            )
            
            if not result['success']:
                all_success = False
                
        except Exception as e:
            PostResult.objects.create(
                post=post,
                provider=provider_name,
                success=False,
                error_message=str(e)
            )
            all_success = False
    
    # Update post status
    if all_success:
        post.status = 'posted'
        post.posted_at = timezone.now()
    else:
        post.status = 'failed'
    
    post.save()
    return all_success

def post_to_single_provider(post, provider_name):
    """Post to a single provider."""
    
    # Get user's token for this provider
    token = OAuthToken.objects.filter(
        provider=provider_name,
        owner=post.user
    ).first()
    
    if not token:
        return {
            'success': False,
            'error_message': f'No {provider_name} account connected'
        }
    
    # Get valid access token
    try:
        provider = OAuth2ProviderFactory.get_provider(provider_name)
        access_token = provider.get_valid_token(token)
        
        if not access_token:
            return {
                'success': False,
                'error_message': f'{provider_name} token expired. Please reconnect.'
            }
    except Exception as e:
        return {
            'success': False,
            'error_message': f'Token validation failed: {str(e)}'
        }
    
    # Post to provider (implement based on provider)
    try:
        if provider_name == 'twitter':
            return post_to_twitter(access_token, post.content)
        elif provider_name == 'linkedin':
            return post_to_linkedin(access_token, post.content, token.user_id)
        elif provider_name == 'github':
            return post_to_github(access_token, post.content)
        else:
            return {
                'success': False,
                'error_message': f'Provider {provider_name} not supported for posting'
            }
    except Exception as e:
        return {
            'success': False,
            'error_message': f'API error: {str(e)}'
        }

def post_to_twitter(access_token, content):
    """Post to Twitter using API v2."""
    import requests
    
    url = "https://api.twitter.com/2/tweets"
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }
    data = {
        "text": content
    }
    
    response = requests.post(url, headers=headers, json=data, timeout=10)
    
    if response.status_code == 201:
        tweet_data = response.json()
        return {
            'success': True,
            'external_id': tweet_data['data']['id'],
            'external_url': f"https://twitter.com/i/web/status/{tweet_data['data']['id']}"
        }
    else:
        return {
            'success': False,
            'error_message': f"Twitter API error: {response.status_code} - {response.text}"
        }

@login_required
def post_detail(request, post_id):
    """View post details and results."""
    post = get_object_or_404(Post, id=post_id, user=request.user)
    results = post.results.all().order_by('provider')
    
    context = {
        'post': post,
        'results': results
    }
    
    return render(request, 'myapp/post_detail.html', context)

@login_required
def retry_failed_providers(request, post_id):
    """Retry posting to failed providers."""
    post = get_object_or_404(Post, id=post_id, user=request.user)
    
    if request.method == 'POST':
        # Get failed providers
        failed_results = post.results.filter(success=False)
        failed_providers = [result.provider for result in failed_results]
        
        if not failed_providers:
            messages.info(request, 'No failed providers to retry')
            return redirect('post_detail', post_id=post.id)
        
        # Delete old failed results
        failed_results.delete()
        
        # Retry posting
        success_count = 0
        for provider_name in failed_providers:
            try:
                result = post_to_single_provider(post, provider_name)
                
                PostResult.objects.create(
                    post=post,
                    provider=provider_name,
                    success=result['success'],
                    external_id=result.get('external_id', ''),
                    external_url=result.get('external_url', ''),
                    error_message=result.get('error_message', '')
                )
                
                if result['success']:
                    success_count += 1
                    
            except Exception as e:
                PostResult.objects.create(
                    post=post,
                    provider=provider_name,
                    success=False,
                    error_message=str(e)
                )
        
        if success_count > 0:
            messages.success(request, f'Successfully posted to {success_count} provider(s)')
            
            # Update post status if all are now successful
            if not post.results.filter(success=False).exists():
                post.status = 'posted'
                post.posted_at = timezone.now()
                post.save()
        else:
            messages.error(request, 'All retry attempts failed')
    
    return redirect('post_detail', post_id=post.id)
```

### Templates

```html
<!-- templates/myapp/dashboard.html -->
{% extends 'base.html' %}

{% block title %}Social Media Dashboard{% endblock %}

{% block content %}
<div class="container">
    <h1>Social Media Dashboard</h1>
    
    <!-- Connected Accounts Status -->
    <div class="row mb-4">
        <div class="col-12">
            <h3>Connected Accounts</h3>
            <div class="row">
                {% for provider, info in connected_accounts.items %}
                <div class="col-md-4 mb-3">
                    <div class="card">
                        <div class="card-body">
                            <h5 class="card-title">
                                {{ provider|title }}
                                {% if info.connected %}
                                    <span class="badge bg-success">Connected</span>
                                {% else %}
                                    <span class="badge bg-danger">Disconnected</span>
                                {% endif %}
                            </h5>
                            {% if info.connected %}
                                <p class="card-text">@{{ info.username }}</p>
                            {% else %}
                                <p class="card-text text-danger">
                                    {% if info.error %}
                                        {{ info.error }}
                                    {% else %}
                                        Not connected
                                    {% endif %}
                                </p>
                                <a href="{{ info.reauth_url }}" class="btn btn-primary btn-sm">
                                    Connect {{ provider|title }}
                                </a>
                            {% endif %}
                        </div>
                    </div>
                </div>
                {% empty %}
                <div class="col-12">
                    <p>No accounts connected. Start by connecting your first account:</p>
                    {% for provider in available_providers %}
                    <a href="/oauth2/{{ provider }}/authorize/" class="btn btn-outline-primary me-2">
                        Connect {{ provider|title }}
                    </a>
                    {% endfor %}
                </div>
                {% endfor %}
            </div>
        </div>
    </div>
    
    <!-- Create New Post -->
    <div class="row mb-4">
        <div class="col-12">
            <h3>Create New Post</h3>
            <form method="post" action="{% url 'create_post' %}">
                {% csrf_token %}
                <div class="mb-3">
                    <label for="content" class="form-label">Post Content</label>
                    <textarea class="form-control" id="content" name="content" rows="4" 
                              maxlength="280" placeholder="What's on your mind?"></textarea>
                    <div class="form-text">280 characters maximum</div>
                </div>
                
                <div class="mb-3">
                    <label class="form-label">Post to:</label>
                    {% for provider, info in connected_accounts.items %}
                        {% if info.connected %}
                        <div class="form-check">
                            <input class="form-check-input" type="checkbox" name="providers" 
                                   value="{{ provider }}" id="provider_{{ provider }}">
                            <label class="form-check-label" for="provider_{{ provider }}">
                                {{ provider|title }} (@{{ info.username }})
                            </label>
                        </div>
                        {% endif %}
                    {% endfor %}
                </div>
                
                <button type="submit" class="btn btn-primary">Post Now</button>
            </form>
        </div>
    </div>
    
    <!-- Recent Posts -->
    <div class="row">
        <div class="col-12">
            <h3>Recent Posts</h3>
            {% if posts %}
            <div class="list-group">
                {% for post in posts %}
                <a href="{% url 'post_detail' post.id %}" class="list-group-item list-group-item-action">
                    <div class="d-flex w-100 justify-between">
                        <h6 class="mb-1">{{ post.content|truncatechars:100 }}</h6>
                        <small>{{ post.created_at|timesince }} ago</small>
                    </div>
                    <p class="mb-1">
                        <span class="badge bg-{{ post.status|yesno:'success,danger,warning' }}">
                            {{ post.get_status_display }}
                        </span>
                        {% for provider in post.providers %}
                            <span class="badge bg-secondary">{{ provider|title }}</span>
                        {% endfor %}
                    </p>
                </a>
                {% endfor %}
            </div>
            {% else %}
            <p>No posts yet. Create your first post above!</p>
            {% endif %}
        </div>
    </div>
</div>
{% endblock %}
```

```html
<!-- templates/myapp/post_detail.html -->
{% extends 'base.html' %}

{% block title %}Post Details{% endblock %}

{% block content %}
<div class="container">
    <div class="row">
        <div class="col-12">
            <nav aria-label="breadcrumb">
                <ol class="breadcrumb">
                    <li class="breadcrumb-item"><a href="{% url 'dashboard' %}">Dashboard</a></li>
                    <li class="breadcrumb-item active">Post Details</li>
                </ol>
            </nav>
            
            <h2>Post Details</h2>
            
            <!-- Post Content -->
            <div class="card mb-4">
                <div class="card-body">
                    <h5 class="card-title">
                        Status: 
                        <span class="badge bg-{{ post.status|yesno:'success,danger,warning' }}">
                            {{ post.get_status_display }}
                        </span>
                    </h5>
                    <p class="card-text">{{ post.content }}</p>
                    <p class="card-text">
                        <small class="text-muted">
                            Created: {{ post.created_at }}
                            {% if post.posted_at %}
                            | Posted: {{ post.posted_at }}
                            {% endif %}
                        </small>
                    </p>
                </div>
            </div>
            
            <!-- Provider Results -->
            <h4>Provider Results</h4>
            {% if results %}
            <div class="row">
                {% for result in results %}
                <div class="col-md-6 mb-3">
                    <div class="card">
                        <div class="card-body">
                            <h6 class="card-title">
                                {{ result.provider|title }}
                                {% if result.success %}
                                    <span class="badge bg-success">Success</span>
                                {% else %}
                                    <span class="badge bg-danger">Failed</span>
                                {% endif %}
                            </h6>
                            
                            {% if result.success %}
                                {% if result.external_url %}
                                    <p><a href="{{ result.external_url }}" target="_blank" class="btn btn-sm btn-outline-primary">
                                        View Post
                                    </a></p>
                                {% endif %}
                                <p class="card-text">
                                    <small class="text-muted">ID: {{ result.external_id }}</small>
                                </p>
                            {% else %}
                                <div class="alert alert-danger">
                                    {{ result.error_message }}
                                </div>
                            {% endif %}
                            
                            <p class="card-text">
                                <small class="text-muted">{{ result.created_at }}</small>
                            </p>
                        </div>
                    </div>
                </div>
                {% endfor %}
            </div>
            
            <!-- Retry Failed Providers -->
            {% if post.results.filter_success_False %}
            <div class="mt-3">
                <form method="post" action="{% url 'retry_failed_providers' post.id %}">
                    {% csrf_token %}
                    <button type="submit" class="btn btn-warning">
                        Retry Failed Providers
                    </button>
                </form>
            </div>
            {% endif %}
            
            {% else %}
            <p>No results available.</p>
            {% endif %}
        </div>
    </div>
</div>
{% endblock %}
```

### URL Configuration

```python
# myapp/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('post/create/', views.create_post, name='create_post'),
    path('post/<int:post_id>/', views.post_detail, name='post_detail'),
    path('post/<int:post_id>/retry/', views.retry_failed_providers, name='retry_failed_providers'),
]
```

## Background Task Integration

For production applications, you should handle social media posting asynchronously:

### Using Celery

```python
# myapp/tasks.py
from celery import shared_task
from django.utils import timezone
import logging

from oauth2_capture.models import OAuthToken
from oauth2_capture.services.oauth2 import OAuth2ProviderFactory
from .models import Post, PostResult

logger = logging.getLogger(__name__)

@shared_task(bind=True, max_retries=3)
def post_to_providers_async(self, post_id):
    """Asynchronously post to all providers for a given post."""
    
    try:
        post = Post.objects.get(id=post_id)
    except Post.DoesNotExist:
        logger.error(f"Post {post_id} not found")
        return {'error': 'Post not found'}
    
    post.status = 'posting'
    post.save()
    
    results = {}
    
    for provider_name in post.providers:
        try:
            result = post_to_provider_sync(post, provider_name)
            results[provider_name] = result
            
            # Save result to database
            PostResult.objects.create(
                post=post,
                provider=provider_name,
                success=result['success'],
                external_id=result.get('external_id', ''),
                external_url=result.get('external_url', ''),
                error_message=result.get('error_message', '')
            )
            
        except Exception as e:
            logger.exception(f"Error posting to {provider_name} for post {post_id}")
            results[provider_name] = {'success': False, 'error': str(e)}
            
            PostResult.objects.create(
                post=post,
                provider=provider_name,
                success=False,
                error_message=str(e)
            )
    
    # Update post status
    successful_posts = sum(1 for result in results.values() if result['success'])
    total_providers = len(post.providers)
    
    if successful_posts == total_providers:
        post.status = 'posted'
        post.posted_at = timezone.now()
    elif successful_posts > 0:
        post.status = 'partial'
    else:
        post.status = 'failed'
    
    post.save()
    
    return {
        'post_id': post_id,
        'successful_posts': successful_posts,
        'total_providers': total_providers,
        'results': results
    }

@shared_task(bind=True, max_retries=3, default_retry_delay=60)
def refresh_expired_tokens(self):
    """Background task to refresh expired tokens."""
    
    from datetime import timedelta
    
    # Find tokens that will expire in the next hour
    soon_expiring = OAuthToken.objects.filter(
        expires_at__lte=timezone.now() + timedelta(hours=1),
        expires_at__gt=timezone.now()
    )
    
    refreshed_count = 0
    failed_count = 0
    
    for token in soon_expiring:
        try:
            provider = OAuth2ProviderFactory.get_provider(token.provider)
            access_token = provider.get_valid_token(token)
            
            if access_token:
                refreshed_count += 1
                logger.info(f"Refreshed token for {token.provider}:{token.user_id}")
            else:
                failed_count += 1
                logger.warning(f"Failed to refresh token for {token.provider}:{token.user_id}")
                
        except Exception as e:
            failed_count += 1
            logger.exception(f"Error refreshing token for {token.provider}:{token.user_id}")
    
    return {
        'refreshed_count': refreshed_count,
        'failed_count': failed_count,
        'total_checked': soon_expiring.count()
    }
```

### Updated Views for Async Processing

```python
# Updated create_post view for async processing
@login_required
def create_post(request):
    """Create a new post with async processing."""
    if request.method == 'POST':
        content = request.POST.get('content', '').strip()
        selected_providers = request.POST.getlist('providers')
        
        if not content or not selected_providers:
            messages.error(request, 'Content and providers are required')
            return redirect('dashboard')
        
        # Create the post
        post = Post.objects.create(
            user=request.user,
            content=content,
            providers=selected_providers,
            status='queued'
        )
        
        # Queue for async processing
        from .tasks import post_to_providers_async
        post_to_providers_async.delay(post.id)
        
        messages.success(request, 'Post queued for publishing!')
        return redirect('post_detail', post_id=post.id)
    
    return redirect('dashboard')
```

This comprehensive example demonstrates:

1. **Complete Django Integration**: Models, views, templates, URLs
2. **Error Handling**: Comprehensive error scenarios and user feedback
3. **Multi-Provider Support**: Handling multiple OAuth providers
4. **Production Patterns**: Async processing, proper error handling
5. **User Experience**: Clear status indicators, retry mechanisms
6. **Security**: Proper token validation and error handling

The example can be extended with additional features like:
- Scheduled posting
- Post analytics
- Content templates
- Team collaboration
- Advanced error recovery
```

## Success Criteria
- [ ] Complete working examples for common use cases
- [ ] Production-ready code with proper error handling
- [ ] Clear documentation with inline explanations
- [ ] Security best practices demonstrated
- [ ] Performance optimization techniques shown
- [ ] Testing examples and patterns included
- [ ] Integration examples with popular Django packages
- [ ] Troubleshooting and debugging guidance