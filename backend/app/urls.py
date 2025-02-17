from django.urls import path, include
from django.shortcuts import render

def home(request):
    return render(request, "index.html") 

urlpatterns = [
    path("", home),
    path("users/", include("users.urls"))
]