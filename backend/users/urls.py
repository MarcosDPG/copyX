from django.urls import path
from . import views

urlpatterns = [
    path('<int:user_id>/', views.user_operations),
    path('', views.user_operations),
]