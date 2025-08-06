# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is `oauth2_capture`, a Django package for capturing and managing OAuth2 tokens from multiple social media providers (Twitter, LinkedIn, GitHub, Reddit, Pinterest, Facebook, Threads). Unlike django-allauth which focuses on user authentication, this package is designed for API integration and ongoing token management.

## Development Environment Setup

### Core Commands
**Note**: uv automatically manages the virtual environment. Always run uv commands from the project root directory where pyproject.toml is located.

- `uv sync --dev` - Install package and all dependencies in development mode (run from project root)
- `cd development && python manage.py migrate` - Run database migrations
- `cd development && python manage.py runserver` - Start development server
- `cd development && python manage.py createsuperuser` - Create admin user

### Environment Configuration
- Copy `development/env.sample` to `development/env` and configure OAuth provider credentials
- Each provider requires `client_id` and `client_secret` from their developer platforms
- Provider setup docs are in `docs/` directory (currently only LinkedIn documented)

### Testing and Linting
**Note**: uv run automatically uses the project's virtual environment

- `ruff check .` - Run linting (configured in pyproject.toml)
- `ruff check --fix .` - Auto-fix linting issues where possible
- `ruff format .` - Format code according to project standards
- `make prerelease` - Run pre-release checks including linting
- Tests are located in `oauth2_capture/tests/` and individual app test files
- **IMPORTANT**: Always use Django's test suite (`uv run python manage.py test`), NEVER use pytest

#### Pre-commit Workflow
**ALWAYS run these commands before every commit to ensure code quality:**

1. `ruff check --fix .` - Auto-fix linting issues
2. `ruff format .` - Format code consistently
3. Run tests to ensure functionality is preserved
4. Commit changes

Note: Test files are excluded from linting rules via pyproject.toml configuration
### Code Coverage
**Note**: Coverage commands must be run from project root directory where pyproject.toml is located

- `uv sync --dev` - Install coverage dependency (run from project root first)
- `uv run coverage run development/manage.py test` - Run tests with coverage measurement
- `uv run coverage report` - Show coverage report in terminal
- `uv run coverage html` - Generate HTML coverage report (opens in `htmlcov/index.html`)
- `uv run coverage json` - Generate JSON coverage report for programmatic analysis
- Coverage configuration is in `pyproject.toml` under `[tool.coverage.*]`

### Release Management
- `make release-dry-run` - Preview version bump
- `make release` - Create release using commitizen (bumps version, creates tag, pushes)

## Architecture

### Core Components

1. **OAuth2Provider Base Class** (`oauth2_capture/services/oauth2.py:87-272`): Abstract base for all OAuth providers with common functionality:
   - Authorization URL generation
   - Token exchange and refresh
   - User info retrieval
   - PKCE support (for Twitter)

2. **Provider Implementations** (`oauth2_capture/services/oauth2.py:273-809`): Concrete implementations for each provider:
   - TwitterOAuth2Provider (with PKCE)
   - LinkedInOAuth2Provider
   - GitHubOAuth2Provider
   - RedditOAuth2Provider (with custom auth headers)
   - PinterestOAuth2Provider
   - FacebookOAuth2Provider

3. **OAuth2ProviderFactory** (`oauth2_capture/services/oauth2.py:782-808`): Factory to get appropriate provider instance

4. **OAuthToken Model** (`oauth2_capture/models.py:7-89`): Django model storing:
   - Access/refresh tokens with expiration
   - Provider-specific user info (profile_json)
   - Associated Django user (owner)
   - Token scopes and metadata

### Key Features

- **Token Refresh**: Automatic refresh of expired tokens via `get_valid_token()` method
- **Rate Limiting**: Built-in retry logic with exponential backoff (`retry_with_backoff()`)
- **Provider Extensibility**: Easy to add new providers by extending OAuth2Provider
- **PKCE Support**: Implemented for providers that require it (Twitter)
- **Multi-user Support**: Each Django user can have multiple tokens per provider

### Configuration

OAuth providers are configured in Django settings via `OAUTH2_CONFIG` dictionary:
```python
OAUTH2_CONFIG = {
    "provider_name": {
        "client_id": "...",
        "client_secret": "...",
        "scope": "...",
        # Provider-specific options
    }
}
```

### URL Structure
- `oauth2/authorize/<provider>/` - Start OAuth flow
- `oauth2/callback/<provider>/` - Handle OAuth callback
- Admin interface available for token management

### Development vs Package Structure
- `development/` - Django project for testing the package
- `oauth2_capture/` - The actual Django app/package
- `demo/` - Demo application showing usage examples

When making changes, ensure compatibility with Django 5.1+ and Python 3.12+ as specified in pyproject.toml.
