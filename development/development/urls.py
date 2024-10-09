from django.contrib import admin
from django.urls import include, path
from django.views.generic import TemplateView

urlpatterns = [
    path("admin/", admin.site.urls),
    path("oauth2_capture/", include("oauth2_capture.urls")),
    path("demo/", include("demo.urls"), name="demo"),
    path("", TemplateView.as_view(template_name="index.html"), name="home"),
]
