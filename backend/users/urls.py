from django.urls import path
from . import views

urlpatterns = [
    path('auth/singup/', views.register, name='singup'),
    path('auth/login/', views.login_view, name='login'),
]