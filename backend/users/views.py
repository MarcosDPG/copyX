from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import User
from .serializers import UserSerializer
from rest_framework import serializers, status
from django.shortcuts import render, redirect
from .forms import RegisterForm
from django.contrib.auth import authenticate, login
from django.contrib import messages

@api_view(['GET'])
def user_operations(request, user_id=None):
    """
    Maneja las operaciones GET
    - GET: Obtiene un usuario por su ID.
    """
    if request.method == 'GET':
        # Lógica para obtener un usuario por su ID
        if user_id:
            try:
                user = User.objects.get(id=user_id)
                serializer = UserSerializer(user)
                return Response(serializer.data)
            except User.DoesNotExist:
                return Response({"error": "Usuario no encontrado"}, status=status.HTTP_404_NOT_FOUND)
        else:
            # Si no se proporciona un ID, devuelve todos los usuarios
            users = User.objects.all()
            serializer = UserSerializer(users, many=True)
            return Response(serializer.data)

def login_view(request):
    if request.method == 'POST':
        user_name = request.POST.get('user_name')
        password = request.POST.get('password')

        user = authenticate(request, user_name=user_name, password=password)

        if user is not None:
            login(request, user)
            request.session.save()
            response = redirect('home')  # Redirige al usuario a la página de inicio
            response.set_cookie('sessionid', request.session.session_key, httponly=True)
            return response
        else:
            messages.error(request, 'Usuario o contraseña incorrectos.')  
            return redirect('login')  # Redirige al formulario de login con el mensaje de error

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
