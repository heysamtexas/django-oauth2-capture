import logging
import sys
import uuid

import requests
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

from demo.services import post_to_twitter, publish_to_linkedin
from oauth2_capture.models import OAuthToken
from oauth2_capture.services.oauth2 import OAuth2ProviderFactory

logger = logging.getLogger(__name__)


def twitter_post(token: str, oauth_token: str) -> tuple:  # noqa: ARG001
    """Post to Twitter."""
    junk = uuid.uuid4().hex
    content = f"Hello, world: {junk}"
    url = post_to_twitter(content, oauth_token)
    return url, f"Tweet created: {url}"


def linkedin_post(token: str, oauth_token: str) -> tuple:
    """Post to LinkedIn."""
    url = publish_to_linkedin(urn=f"urn:li:person:{token.user_id}", access_token=oauth_token, content="Hello, world!")
    return url, f"LinkedIn Post created: {url}"


def reddit_post(token: str, oauth_token: str) -> tuple:  # noqa: ARG001
    """Post to Reddit."""
    subreddit = "testingground4bots"
    junk = uuid.uuid4().hex
    title = f"Test Post {junk}"
    content = f"Hello, world: {junk}"

    headers = {"Authorization": f"Bearer {oauth_token}", "User-Agent": "OAuth2Demo/1.0"}
    data = {"sr": subreddit, "kind": "self", "title": title, "text": content}

    response = requests.post("https://oauth.reddit.com/api/submit", headers=headers, data=data, timeout=10)

    if response.status_code == 200:  # noqa: PLR2004
        submission_data = response.json()
        post_id = submission_data.get("data", {}).get("id", "")
        url = f"https://www.reddit.com/r/{subreddit}/comments/{post_id}"
        return url, f"Reddit post created: {url}"
    logger.error("Reddit post failed: %s", response.text)
    return "", f"Reddit post failed: {response.status_code}"


@require_POST
@csrf_exempt
@login_required
def social_post(request: HttpRequest, provider: str, slug: str) -> HttpResponse:
    """Handle social media posts for different providers."""
    token = get_object_or_404(OAuthToken, slug=slug)
    oa2 = OAuth2ProviderFactory.get_provider(provider).get_valid_token(token)

    # Look up the appropriate function using naming convention
    post_function_name = f"{provider}_post"
    current_module = sys.modules[__name__]
    post_function = getattr(current_module, post_function_name, None)

    if post_function is None:
        messages.error(request, f"Unsupported provider: {provider}")
        return redirect("/")

    url, msg = post_function(token, oa2)
    logger.info(msg)
    messages.success(request, msg)
    return redirect("/")


@login_required
def index(request: HttpRequest) -> HttpResponse:
    """Render the index page."""
    tokens = OAuthToken.objects.filter(owner=request.user)
    return render(request, "demo.html", {"tokens": tokens})
