from django.urls import path
from . import views

urlpatterns = [
    path('likes/', views.like_operations),
    path("likes/<str:like_id>", views.delete_like),
]