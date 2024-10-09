import json
import logging

import requests

logger = logging.getLogger(__name__)


class TwitterError(Exception):
    """Exception raised when a post cannot be published to Twitter."""


def post_to_twitter(content: str, access_token: str) -> str:
    """Post a tweet to Twitter.

    Args:
    ----
        content (str): The content of the tweet.
        access_token (str): The access token for the Twitter account.

    Returns:
    -------
        str: The URL of the published tweet.

    """
    logger.debug("Posting to Twitter")

    url = "https://api.twitter.com/2/tweets"
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json",
    }
    payload = {"text": content}

    response = requests.post(url, json=payload, headers=headers, timeout=30)

    if response.status_code == 201:  # noqa: PLR2004
        tweet_data = response.json()
        tweet_id = tweet_data["data"]["id"]
        return f"https://twitter.com/user/status/{tweet_id}"

    msg = f"Failed to post tweet {response.text}"
    raise TwitterError(msg)


class PublishLinkedInError(Exception):
    """Exception raised when a post cannot be published to LinkedIn."""


def publish_to_linkedin(urn: str, access_token: str, content: str) -> str:
    """Publish a post to LinkedIn.

    Args:
    ----
        urn (str): The URN of the LinkedIn account.
        access_token (str): The access token for the LinkedIn account.
        content (str): The content of the post.

    Returns:
    -------
        str: The URL of the published post.

    """
    logger.debug("Publishing to LinkedIn")
    url = "https://api.linkedin.com/v2/ugcPosts"

    headers = {
        "Authorization": f"Bearer {access_token}",
        "X-Restli-Protocol-Version": "2.0.0",
        "Content-Type": "application/json",
    }
    payload = {
        "author": urn,
        "lifecycleState": "PUBLISHED",
        "specificContent": {
            "com.linkedin.ugc.ShareContent": {
                "shareCommentary": {"text": content},
                "shareMediaCategory": "NONE",
            }
        },
        "visibility": {"com.linkedin.ugc.MemberNetworkVisibility": "PUBLIC"},
    }

    r = requests.post(url, headers=headers, data=json.dumps(payload), timeout=30)
    try:
        r.raise_for_status()
    except requests.exceptions.RequestException as e:
        msg = "Could not publish to LinkedIn"
        logger.exception("Response Status Code: %s", r.status_code)
        logger.exception("Response Content: %s", r.content)

        raise PublishLinkedInError(msg) from e

    output = r.json()["id"]
    return f"https://www.linkedin.com/feed/update/{output}/"
