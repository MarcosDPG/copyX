from django.urls import path
from . import views
from .views import register
from .views import login_view

urlpatterns = [
    path("", views.create_users, name="create-users"),
    path('register/', register, name='register'),
    path('login/', login_view, name='login'),
]