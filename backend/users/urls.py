from django.urls import path
from . import views

urlpatterns = [
    path('', views.user_operations, name="users"),
    path('auth/singup/', views.register, name='singup'),
    path('auth/login/', views.login_view, name='login'),
]