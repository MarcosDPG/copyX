from django.urls import path, include
from django.contrib import admin
from . import views

urlpatterns = [
    path("", views.home, name="start"),
    path("welcome/", views.welcome, name="welcome"),
    path("home/", views.home, name="home"),
    path("profile/", views.profile, name="profile_auth"),
    path("profile/<str:user_id>", views.profile, name="profile_user_id"),
    path("settings/", views.settings_view, name="settings"),
    path("search/", views.search_view, name="search"),
    path("compose/post/", views.home, name="compose_post"),
    path('settings/<str:option>/', views.settings_partial, name='settings_partial'),
    path('admin/', admin.site.urls),
    path("users/", include("users.urls")),
    path("tweets/", include("publications.urls"))
]