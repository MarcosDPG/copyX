from django.urls import path, include
from app.views import base, home, profile, settings_view, settings_partial
urlpatterns = [
    path("", base),
    path("home/", home, name="home"),
    path("profile/", profile, name="profile_auth"),
    path("profile/<str:user_id>", profile, name="profile_user_id"),
    path("settings/", settings_view, name="settings"),
    path("compose/post/", home, name="compose_post"),
    path('settings/<str:option>/', settings_partial, name='settings_partial'),
]