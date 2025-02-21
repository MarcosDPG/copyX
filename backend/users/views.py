from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import User
from .serializers import UserSerializer
from rest_framework import status
from django.shortcuts import render, redirect
from .forms import RegisterForm
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.contrib.auth import logout
from django.shortcuts import redirect
from django.http import JsonResponse

@api_view(['GET'])
def user_operations(request, user_id=None):
    """
    Maneja las operaciones GET
    - GET: Obtiene un usuario por su ID.
    """
    if request.method == 'GET':
        # Get an user for id
        if user_id:
            try:
                data_user = retrieve_user(user_id)
                return Response(data=data_user)
            except User.DoesNotExist:
                return Response({"error": "Usuario no encontrado"}, status=status.HTTP_404_NOT_FOUND)
        else:
            # If there is no id, it returns all users
            try:
                users = User.objects.all()
                serializer = UserSerializer(users, many=True)
                return Response(serializer.data)
            except Exception as e:
                return Response({"Error": str(e)})

def login_view(request):
    if request.method == 'POST':
        user_name = request.POST.get('user_name')
        password = request.POST.get('password')

        user = authenticate(request, user_name=user_name, password=password)

        if user is not None:
            login(request, user)
            request.session.save()
            response = JsonResponse({"message": "Inicio de sesión exitoso"}, status=200) #Se devuelve json response para poder capturar el error e informar al usuario
            response.set_cookie('sessionid', request.session.session_key, httponly=True)
            return response
        else:
            return JsonResponse({"message": "Usuario o contraseña incorrectos."}, status=400)

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

def logout_view(request):
    logout(request)  # Cierra la sesión del usuario
    return redirect('login')  # Redirige al usuario a la página de inicio de sesión

def delete_account(request):
    if request.method == 'POST':
        # Obtén la contraseña del formulario
        password = request.POST.get('password')

        # Verifica la contraseña del usuario
        user = authenticate(user_name=request.user.user_name, password=password)

        if user is not None:
            # Si la contraseña es correcta, elimina la cuenta
            user.delete()
            logout(request)  # Cierra la sesión del usuario
            messages.success(request, 'Tu cuenta ha sido eliminada correctamente.')
            return redirect('login')  # Redirige al usuario a la página de inicio de sesión
        else:
            # Si la contraseña es incorrecta, muestra un mensaje de error
            messages.error(request, 'Contraseña incorrecta. No se pudo eliminar la cuenta.')

    # Si no es una solicitud POST, muestra el formulario de eliminación de cuenta
    return redirect('settings')  # Redirige a la página de configuración

def retrieve_user(id):
    try:
        user = User.objects.get(user_id=id)
        serializer = UserSerializer(user)
        return serializer.data
    except User.DoesNotExist:
        return {
        "name": "",
        "user_name":"",
        "posts_count": 0
        }