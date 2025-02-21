from django.urls import path
from . import views

urlpatterns = [
    path('', views.tweet_operations, name="tweet"),
    path('<str:user_id>/', views.tweet_operations, name="tweet_user_id"),
]