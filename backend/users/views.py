from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import User
from .serializers import UserSerializer
from rest_framework import status

@api_view(['GET', 'POST'])
def user_operations(request, user_id=None):
    """
    Maneja las operaciones GET y POST para los usuarios.
    - GET: Obtiene un usuario por su ID.
    - POST: Crea un nuevo usuario.
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
                print(users)
                serializer = UserSerializer(users, many=True)
                return Response(serializer.data)
            except Exception as e:
                return Response({"Error": str(e)})

    elif request.method == 'POST':
        # Lógica para crear un nuevo usuario
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

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
