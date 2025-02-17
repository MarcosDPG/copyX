from django.urls import path
from app.views import base, home, profile, settings_view

urlpatterns = [
    path("", base),
    path("home/", home, name="home"),
    path("profile/", profile, name="profile"),
    path("settings/", settings_view, name="settings"),
]