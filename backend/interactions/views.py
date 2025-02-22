from django.contrib.contenttypes.models import ContentType
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.response import Response
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import IsAuthenticated

from rest_framework import status
from rest_framework.decorators import api_view

from publications.models import Tweet, Comment
from .models import Like
from .serializer import LikeSerializer

@api_view(['POST'])
@authentication_classes([SessionAuthentication])
@permission_classes([IsAuthenticated])
def like_operations(request):
    like_data = request.data
    user = request.user

    # Check if the user has already liked the object
    if Like.objects.filter(user=user, object_id=like_data["object_id"]).exists():
        return Response({"message": "Ya le diste like a este objeto"}, status=status.HTTP_400_BAD_REQUEST)
    try:
        # Create a like for the object
        if like_data["type"] == 1:
            like = create_comment(like_data["object_id"], user)
        else:
            like = create_tweet(like_data["object_id"], user)

        serializer = LikeSerializer(like)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    except Tweet.DoesNotExist:
        return Response({"message": "Tweet no encontrado"}, status=status.HTTP_404_NOT_FOUND)
    except Comment.DoesNotExist:
        return Response({"message": "Comentario no encontrado"}, status=status.HTTP_404_NOT_FOUND)

def create_comment(comment_id, user):
    # Get the content type for the Comment model
    comment_content_type = ContentType.objects.get_for_model(Comment)

    # Create a Like for a specific Comment
    comment = Comment.objects.get(comment_id=comment_id)
    like = Like.objects.create(
        user=user,
        content_type=comment_content_type,
        object_id=comment.comment_id
    )
    return like

@api_view(['DELETE'])
@authentication_classes([SessionAuthentication])
@permission_classes([IsAuthenticated])
def delete_like(request, like_id):
    try:
        # Check if the user has already liked the object
        like = Like.objects.get(like_id=like_id, user=request.user)
        like.delete()
        return Response({"message": "Like eliminado"}, status=status.HTTP_200_OK)
    except Like.DoesNotExist:
        return Response({"message": "Like no encontrado"}, status=status.HTTP_404_NOT_FOUND)

def create_tweet(tweet_id, user):
    # Obtener el contenido tipo para el modelo Tweet
    tweet_content_type = ContentType.objects.get_for_model(Tweet)

    # Crear un Like para un Tweet específico
    tweet = Tweet.objects.get(tweet_id=tweet_id)
    like = Like.objects.create(
        user=user,  # Instancia del usuario que da el like
        content_type=tweet_content_type,
        object_id=tweet.tweet_id
    )
    return like