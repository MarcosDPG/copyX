from django.urls import path
from . import views

urlpatterns = [
    path('tweets/', views.tweet_operations, name="tweet"),
    path('tweets/post/<str:post_id>/', views.tweet_operations, name="tweet_post_id"),
    path('tweets/<str:user_id>/', views.tweet_operations, name="tweet_user_id"),
    path('retweet/', views.retweet_operations, name="retweet"),
    path('retweet/<str:retweet_id>', views.retweet_operations, name="retweet-delete"),
    path('users/retweets/<str:user_id>/', views.retrieve_retweet_info, name="retweet-user"),
    path('users/likes/<str:user_id>', views.retrieve_liked_post, name="user-like"),
    path('comments/', views.comment_operations, name="comment"),
    path('comments/<str:comment_id>', views.comment_operations, name="comment-delete"),
    path('comments/tweet/<str:tweet_id>', views.comment_operations, name="tweet-comment"),
]