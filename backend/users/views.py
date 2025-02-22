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
from django.http import JsonResponse
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.decorators import login_required
from django.db.models import Q
import json

@api_view(['GET'])
def user_operations(request, user_id=None):
    """
    Maneja las operaciones GET:
    - GET con `user_id`: Obtiene un usuario por su ID (JSON).
    - GET sin `user_id`: Devuelve todos los usuarios en JSON o en HTML si `request.accepts("text/html")`.
    """
    try:
        if user_id:
            # Obtener un usuario por su ID (JSON)
            data_user = retrieve_user(user_id)
            return Response(data=data_user)

        else:
            # Obtener todos los usuarios
            search_query = request.GET.get('search_users', '')  # Obtener parámetro de búsqueda
            users = User.objects.filter(user_name__icontains=search_query) if search_query else User.objects.all()
            
            serializer = UserSerializer(users, many=True)
            user_data = json.loads(json.dumps(serializer.data, default=str))
        
            return render(request, "partials/user_card_list.html", {"users": user_data, "empty_message": "No se encontraron usuarios."})

            # Si no, devolver JSON como antes
            return Response(user_data)

    except User.DoesNotExist:
        return Response({"error": "Usuario no encontrado"}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({"Error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


def login_view(request):
    if request.user.is_authenticated:
        return redirect('home')

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
    if request.user.is_authenticated:
        return redirect('home')

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
    return redirect('login')  # Redirige al usuario a la página de login

@login_required
def edit_name(request):
    if request.method == 'POST':
        # Obtén el nuevo nombre del formulario
        new_name = request.POST.get('name')

        # Actualiza el nombre del usuario
        user = request.user
        user.name = new_name
        user.save()

        messages.success(request, 'Tu nombre ha sido actualizado correctamente.')
        return redirect('settings')  # Redirige a la página de configuración

    # Si no es una solicitud POST, muestra el formulario de edición de nombre
    return redirect('settings')

@login_required
def edit_birth_date(request):
    if request.method == 'POST':
        # Obtén la nueva fecha de nacimiento del formulario
        day = request.POST.get('day')
        month = request.POST.get('month')
        year = request.POST.get('year')

        # Combina los valores en una fecha (formato: YYYY-MM-DD)
        new_birth_date = f"{year}-{month}-{day}"

        # Actualiza la fecha de nacimiento del usuario
        user = request.user
        user.birth_date = new_birth_date
        user.save()

        messages.success(request, 'Tu fecha de nacimiento ha sido actualizada correctamente.')
        return redirect('settings')  # Redirige a la página de configuración

    # Si no es una solicitud POST, muestra el formulario de edición de fecha de nacimiento
    return redirect('settings')

def change_password(request):
    if request.method == 'POST':
        # Crea un formulario de cambio de contraseña con los datos enviados
        form = PasswordChangeForm(request.user, request.POST)

        if form.is_valid():
            # Si el formulario es válido, cambia la contraseña
            user = form.save()
            update_session_auth_hash(request, user)  # Actualiza la sesión para evitar que el usuario sea desconectado
            messages.success(request, 'Tu contraseña ha sido cambiada correctamente.')
            return redirect('settings')  # Redirige a la página de configuración
        else:
            # Si el formulario no es válido, muestra los errores
            messages.error(request, 'Por favor, corrige los errores.')
    else:
        # Si no es una solicitud POST, muestra el formulario de cambio de contraseña
        form = PasswordChangeForm(request.user)

    return render(request, 'change_password.html', {'form': form})
@login_required
def edit_username(request):
    if request.method == 'POST':
        # Obtén el nuevo nombre de usuario del formulario
        new_username = request.POST.get('username')

        # Verifica si el nuevo nombre de usuario ya está en uso
        if User.objects.filter(user_name=new_username).exists():
            messages.error(request, 'El nombre de usuario ya está en uso. Por favor, elige otro.')
        else:
            # Actualiza el nombre de usuario
            user = request.user
            user.user_name = new_username
            user.save()

            messages.success(request, 'Tu nombre de usuario ha sido actualizado correctamente.')
            return redirect('settings')  # Redirige a la página de configuración

    # Si no es una solicitud POST, muestra el formulario de edición de nombre de usuario
    return redirect('settings')

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
            return redirect('welcome')  # Redirige al usuario a la página de bienvenida
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

def list_users(request):
    search = request.GET.get("search_users", "")

    users = User.objects.filter(
        Q(user_name__icontains=search) |
        Q(name__icontains=search)
    ).distinct()

    return JsonResponse({"users": list(users.values("name", "user_name"))})