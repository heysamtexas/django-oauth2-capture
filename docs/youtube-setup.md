# Setup a YouTube application for use with OAuth2

1. Go to the [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select an existing one
3. Enable the YouTube Data API v3:
   - Navigate to "APIs & Services" > "Library"
   - Search for "YouTube Data API v3"
   - Click on it and click "Enable"
4. Create OAuth 2.0 credentials:
   - Go to "APIs & Services" > "Credentials"
   - Click "Create Credentials" > "OAuth client ID"
   - Configure the OAuth consent screen if prompted (External user type is fine for testing)
   - Select "Web application" as the application type
   - Add authorized redirect URIs (use your HTTPS tunnel/proxy URL, see "Local Development HTTPS Setup" below)
5. Configure OAuth consent screen:
   - Add your app name, user support email, and developer contact information
   - Under "Scopes", add the YouTube Data API v3 scope: `https://www.googleapis.com/auth/youtube.upload`
   - For testing, add your test users under "Test users"

You will need the **Client ID** and **Client Secret** from the OAuth 2.0 client.

## Important Notes

- The default scope `https://www.googleapis.com/auth/youtube.upload` allows uploading videos to YouTube
- For broader access, you can use `https://www.googleapis.com/auth/youtube` (full access) or other specific scopes
- YouTube OAuth requires that users have a YouTube channel associated with their Google account
- The app will need to go through Google's verification process for production use with unverified users

## Local Development HTTPS Setup

**Google OAuth requires HTTPS redirect URIs.** For local development, you have several options:

### Option 1: ngrok (Recommended)
1. Install ngrok: https://ngrok.com/download
2. Start your Django server: `python manage.py runserver`
3. In another terminal, start ngrok: `ngrok http 8000`
4. ngrok will provide an HTTPS URL like: `https://abc123.ngrok.io`
5. Update your Google OAuth redirect URI to: `https://abc123.ngrok.io/oauth2_capture/youtube/callback/`
6. Set environment variable: `FORCE_HTTPS_REDIRECT=true`

**Note**: Free ngrok URLs change each restart. Paid plans offer persistent domains.

### Option 2: localhost.run (Free Alternative)
1. Start your Django server: `python manage.py runserver`
2. In another terminal: `ssh -R 80:localhost:8000 ssh.localhost.run`
3. You'll get an HTTPS URL like: `https://randomstring.localhost.run`
4. Update your Google OAuth redirect URI to: `https://randomstring.localhost.run/oauth2_capture/youtube/callback/`
5. Set environment variable: `FORCE_HTTPS_REDIRECT=true`

### Option 3: Reverse Proxy
If you already have a reverse proxy (nginx, caddy) with SSL termination:
1. Configure your proxy to forward to `localhost:8000`
2. Update your Google OAuth redirect URI to use your proxy domain
3. Set environment variable: `FORCE_HTTPS_REDIRECT=true`

### Environment Configuration

In your `development/env` file, set:
```
FORCE_HTTPS_REDIRECT=true
CSRF_TRUSTED_ORIGINS=https://your-tunnel-or-proxy-domain.com
```

This ensures OAuth redirect URIs use HTTPS as required by Google.

## Available Scopes

- `https://www.googleapis.com/auth/youtube.readonly` - View your YouTube account
- `https://www.googleapis.com/auth/youtube.upload` - Upload videos to YouTube (default scope)
- `https://www.googleapis.com/auth/youtube` - Manage your YouTube account
- `https://www.googleapis.com/auth/youtube.force-ssl` - View your YouTube account (requires SSL)

## Testing

Make sure to test with a Google account that has an associated YouTube channel, as the API requires this to return user information.
