from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import User
from .serializers import UserSerializer
from rest_framework import serializers, status

@api_view(['POST'])
def create_users(request):
    user = UserSerializer(data=request.data)

    # validating for already existing users
    if User.objects.filter(**request.data).exists():
        raise serializers.ValidationError("The User already exists")

    if user.is_valid():
        user.save()
        return Response(status=status.HTTP_201_CREATED)
    else:
        return Response(status=status.HTTP_404_NOT_FOUND)
