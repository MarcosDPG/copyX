from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import User
from .serializers import UserSerializer
from rest_framework import serializers, status
from django.shortcuts import render, redirect
from .forms import RegisterForm
from django.contrib.auth import authenticate, login
from django.contrib import messages

def login_view(request):
    if request.method == 'POST':
        # Obtén los datos del formulario
        username = request.POST.get('username')
        password = request.POST.get('password')

        # Autentica al usuario
        user = authenticate(request, username=username, password=password)

        if user is not None:
            # Si las credenciales son válidas, inicia sesión
            login(request, user)
            return redirect('home')  # Redirige al home después del login
        else:
            # Si las credenciales son inválidas, muestra un mensaje de error
            messages.error(request, 'Usuario o contraseña incorrectos.')
            return redirect('login')  # Redirige de nuevo al formulario de login
    else:
        # Si no es una solicitud POST, muestra el formulario de login
        return render(request, 'login.html')

def register(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        birth_date = request.POST.get('birth_date')
        user_name = request.POST.get('user_name')
        email = request.POST.get('email')
        password = request.POST.get('password')

        data = {
            'name': name,
            'birth_date': birth_date,
            'user_name': user_name,
            'email': email,
            'password': password,
        }

        form = RegisterForm(data)

        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = RegisterForm()

    return render(request, 'register.html', {'form': form})
