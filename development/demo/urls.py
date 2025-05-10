from django.urls import path

from .views import index, social_post

app_name = "demo"

urlpatterns = [
    path("", index, name="index"),
    path("<str:provider>/<slug:slug>/", social_post, name="social_post"),
]
