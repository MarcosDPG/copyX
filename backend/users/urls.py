from django.urls import path
from . import views
from .views import logout_view, delete_account, change_password,edit_name, edit_birth_date, edit_username
from .views import list_users

urlpatterns = [
    path('<int:user_id>/', views.user_operations, name="user_id"),
    path('', views.user_operations, name="user"),
    path('auth/singup/', views.register, name='singup'),
    path('auth/login/', views.login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('delete-account/', delete_account, name='delete_account'),
    path('change-password/', change_password, name='change_password'),
    path('edit-name/', edit_name, name='edit_name'),
    path('edit-birth-date/', edit_birth_date, name='edit_birth_date'),
    path('edit-username/', edit_username, name='edit_username'),
    path('search/', list_users, name='search'),

]