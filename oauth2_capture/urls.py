from django.urls import path

from oauth2_capture.views import (
    DeleteOAuthTokenView,
    OAuthListView,
    initiate_oauth2,
    oauth2_callback,
)

app_name = "oauth2_capture"

urlpatterns = [
    path("", OAuthListView.as_view(), name="list"),
    path("<slug:slug>/revoke/", DeleteOAuthTokenView.as_view(), name="revoke"),
    path("<str:provider>/connect/", initiate_oauth2, name="initiate_oauth2"),
    path("<str:provider>/callback/", oauth2_callback, name="oauth2_callback"),
]
