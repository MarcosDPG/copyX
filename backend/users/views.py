from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import User
from .serializers import UserSerializer
from rest_framework import serializers, status

@api_view(['GET', 'POST'])
def user_operations(request, user_id=None):
    """
    Maneja las operaciones GET y POST para los usuarios.
    - GET: Obtiene un usuario por su ID.
    - POST: Crea un nuevo usuario.
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

    elif request.method == 'POST':
        # Lógica para crear un nuevo usuario
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)