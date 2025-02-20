from django.urls import path, include
from django.contrib import admin
from app.views import welcome, home, profile, settings_view, settings_partial, search_view, login, register

urlpatterns = [
    path("", home, name="start"),
    path("welcome/", welcome, name="welcome"),
    path("home/", home, name="home"),
    path("login/", login, name="login"),
    path("register/", register, name="register"),
    path("profile/", profile, name="profile"),
    path("settings/", settings_view, name="settings"),
    path("search/", search_view, name="search"),
    path("compose/post/", home, name="compose_post"),
    path('settings/<str:option>/', settings_partial, name='settings_partial'),
    path('admin/', admin.site.urls),
    path("users/", include("users.urls")),
]