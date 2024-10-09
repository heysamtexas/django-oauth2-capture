from django.urls import path

from .views import index, linkedin_post, x_post

app_name = "demo"

urlpatterns = [
    path("", index, name="index"),
    path("x/<slug:slug>/", x_post, name="x"),
    path("linkedin/<slug:slug>/", linkedin_post, name="linkedin"),
]
