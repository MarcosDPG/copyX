from django.urls import path
from django.shortcuts import render

def home(request):
    return render(request, "index.html") 
def login(request):
    return render(request, "login.html") 
def register(request):
    return render(request, "register.html") 

urlpatterns = [
    path("", home, name = "home"),
    path("login/", login, name = "login"),
    path("register/", register, name = "register"),

]