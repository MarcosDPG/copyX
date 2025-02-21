from django.urls import path
from . import views

urlpatterns = [
    path('', views.tweet_operations),
    path('<str:user_id>/', views.tweet_operations),
]