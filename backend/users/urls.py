from django.urls import path
from . import views
from .views import logout_view
from .views import delete_account

urlpatterns = [
    path('<int:user_id>/', views.user_operations, name="user_id"),
    path('', views.user_operations, name="user"),
    path('auth/singup/', views.register, name='singup'),
    path('auth/login/', views.login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('delete-account/', delete_account, name='delete_account'),
]