from django.urls import path
from django.shortcuts import render

def home(request):
    return render(request, "index.html") 

urlpatterns = [
    path("", home),
]