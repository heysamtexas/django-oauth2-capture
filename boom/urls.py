from django.urls import path

from boom.views import (
    DeleteOAuthTokenView,
    OAuthListView,
    initiate_oauth2,
    oauth2_callback,
)

app_name = "boom"

urlpatterns = [
    path("", OAuthListView.as_view(), name="list"),
    path("<slug:slug>/revoke/", DeleteOAuthTokenView.as_view(), name="revoke"),
    path("<str:provider>/conntect/", initiate_oauth2, name="initiate_oauth2"),
    path("<str:provider>/callback/", oauth2_callback, name="oauth2_callback"),
]
