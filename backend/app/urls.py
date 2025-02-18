from django.urls import path, include
from app.views import base, home, profile, settings_view, settings_partial, search_view
urlpatterns = [
    path("", base),
    path("home/", home, name="home"),
    path("profile/", profile, name="profile"),
    path("settings/", settings_view, name="settings"),
    path("search/", search_view, name="search"),
    path("compose/post/", home, name="compose_post"),
    path('settings/<str:option>/', settings_partial, name='settings_partial'),
    path("users/", include("users.urls"))
]