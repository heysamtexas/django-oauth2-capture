import logging
import uuid

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from services.oauth2 import OAuth2ProviderFactory

from demo.services import post_to_twitter, publish_to_linkedin
from oauth2_capture.models import OAuthToken

logger = logging.getLogger(__name__)


@login_required
def index(request: HttpRequest) -> HttpResponse:
    """Render the index page."""
    tokens = OAuthToken.objects.filter(owner=request.user)
    return render(request, "demo.html", {"tokens": tokens})


@require_POST
@csrf_exempt
@login_required
def x_post(request: HttpRequest, slug: str) -> HttpResponse:
    """Handle POST requests."""
    token = get_object_or_404(OAuthToken, slug=slug)
    oa2 = OAuth2ProviderFactory.get_provider("twitter").get_valid_token(token)
    junk = uuid.uuid4().hex
    url = post_to_twitter(f"Hello, world: {junk}", oa2)
    msg = f"Tweet created: {url}"
    logger.info(msg)
    messages.success(request, msg)
    return redirect("/")


@require_POST
@csrf_exempt
@login_required
def linkedin_post(request: HttpRequest, slug: str) -> HttpResponse:
    """Create a linkedin post. There are no refresh tokens available for linkedin. re-auth after 60 days."""
    token = get_object_or_404(OAuthToken, slug=slug)
    oa2 = OAuth2ProviderFactory.get_provider("linkedin").get_valid_token(token)
    url = publish_to_linkedin(
        urn=f"urn:li:person:{token.user_id}",
        access_token=oa2,
        content="Hello, world!",
    )

    messages.success(request, f"Linkedin Post created: {url} ")
    return redirect("/")
