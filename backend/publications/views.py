import copy
import json

from django.utils import timezone
from django.contrib.contenttypes.models import ContentType
from django.db.models import Count, Subquery, OuterRef, Value
from django.db.models.functions import Coalesce
from django.shortcuts import render

from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from interactions.models import Like
from users.models import User
from .models import Tweet, Retweet, Comment
from .serializers import TweetSerializer, RetweetSerializer, CommentSerializer

@api_view(['GET','POST'])
@authentication_classes([SessionAuthentication])
@permission_classes([IsAuthenticated])
def tweet_operations(request, user_id=None, post_id=None, postman=None):
    if request.method == 'GET':
        try:
            if post_id:
                tweetSerializer = retrieve_information_unique_post(post_id=post_id)
            elif user_id:
                tweetSerializer = retrieve_information(user_id=user_id)
            else:
                tweetSerializer = retrieve_information(user=request.user, is_in_home=True)
            tweet_data = json.loads(json.dumps(tweetSerializer.data, default=str))
            return render(request, "partials/posts_list.html", {"posts": tweet_data, "empty_message": "No post yet..."})

        except Exception as e:
            return Response({"Error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    elif request.method == 'POST':
        tweetSerializer = TweetSerializer(data=request.data, context={'request': request})
        if tweetSerializer.is_valid():
            tweetSerializer.save()
            return Response(tweetSerializer.data, status=status.HTTP_201_CREATED)
        return Response(tweetSerializer.errors,status=status.HTTP_400_BAD_REQUEST)

def get_delta_created(fecha):
    delta = timezone.now() - fecha
    days = delta.days
    seconds = delta.seconds
    hours = seconds // 3600
    minutes = seconds // 60

    if days > 0:
        return f"{days}D"
    elif hours > 0:
        return f"{hours}Hrs"
    elif minutes > 0:
        return f"{minutes}min"
    else:
        return f"{seconds}seg"

@api_view(['POST','DELETE'])
@authentication_classes([SessionAuthentication])
@permission_classes([IsAuthenticated])
def retweet_operations(request, retweet_id=None):
    user = request.user
    if request.method == 'POST':
        retweetSerializer = RetweetSerializer(data=request.data)

        if not retweetSerializer.is_valid():
            return Response(retweetSerializer.errors, status=status.HTTP_400_BAD_REQUEST)

        # Get the tweet to retweet
        tweet = retweetSerializer.validated_data.get('tweet')
        # Check if the user has already retweeted the tweet
        if Retweet.objects.filter(user=user, tweet=tweet).exists():
            return Response({"Error": "Ya hiciste un retweet a este post"}, status=status.HTTP_400_BAD_REQUEST)

        retweetSerializer.save(user=user)
        return Response(retweetSerializer.data, status=status.HTTP_201_CREATED)
    if request.method == 'DELETE':
        try:
            Retweet.objects.get(user=user, retweet_id=retweet_id).delete()
            return Response({"message": "Retweet eliminado"}, status=status.HTTP_200_OK)
        except Retweet.DoesNotExist:
            return Response({"Error": "El retweet no existe"}, status=status.HTTP_404_NOT_FOUND)

@api_view(['GET','POST','DELETE'])
@authentication_classes([SessionAuthentication])
@permission_classes([IsAuthenticated])
def comment_operations(request, comment_id=None, tweet_id=None):
    user = request.user
    if request.method == 'POST':
        commentSerializer = CommentSerializer(data=request.data)

        if not commentSerializer.is_valid():
            return Response(commentSerializer.errors, status=status.HTTP_400_BAD_REQUEST)

        commentSerializer.save(user=user)
        return Response(commentSerializer.data, status=status.HTTP_201_CREATED)
    if request.method == 'DELETE':
        try:
            Comment.objects.get(user=user, comment_id=comment_id).delete()
            return Response({"message": "Comentario eliminado"}, status=status.HTTP_200_OK)
        except Comment.DoesNotExist:
            return Response({"Error": "El comentario no existe"}, status=status.HTTP_404_NOT_FOUND)
    if request.method == 'GET':
        #try:
        comments = Comment.objects.filter(tweet_id=tweet_id).order_by('-created_at').select_related('user')
        contentType = ContentType.objects.get_for_model(Comment)
        for comment in comments:
            comment.user_name_commenter = comment.user.user_name
            comment.name = comment.user.name
            comment.delta_created = get_delta_created(comment.created_at)
            comment.like_count = Like.objects.filter(content_type=contentType, object_id=comment.comment_id).count()
            comment.id_like = Like.objects.filter(content_type=contentType, object_id=comment.comment_id,user=user).values("like_id").first()

        commentSerializer = CommentSerializer(comments, many=True)
        tweet_data = json.loads(json.dumps(commentSerializer.data, default=str))
        return render(request, "partials/posts_list.html", {"posts": tweet_data, "empty_message": "No post yet..."})
        #except Exception as e:
         #   return Response({"Error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
@authentication_classes([SessionAuthentication])
@permission_classes([IsAuthenticated])
def retrieve_retweet_info(request, user_id):
    user = User.objects.get(user_id=user_id)
    # Get all the necessary information for the retweets
    tweetSerializer = retrieve_information(user=user, is_retweet=True)
    tweet_data = json.loads(json.dumps(tweetSerializer.data, default=str))
    return render(request, "partials/posts_list.html", {"posts": tweet_data, "empty_message": "No post yet..."})

@api_view(['GET'])
@authentication_classes([SessionAuthentication])
@permission_classes([IsAuthenticated])
def retrieve_liked_post(request, user_id):
    user = User.objects.get(user_id=user_id)
    tweetSerializer = retrieve_information(user=user, is_posts_liked=True)
    tweet_data = json.loads(json.dumps(tweetSerializer.data, default=str))
    return render(request, "partials/posts_list.html", {"posts": tweet_data, "empty_message": "No post yet..."})

# Return all the necessary information for the tweets, is_retweet means that the user is looking for his retweets
def retrieve_information(user=None, user_id=None, is_retweet=False, is_posts_liked=False, is_in_home=False):
    # Get the content type for the Tweet model
    tweet_content_type = ContentType.objects.get_for_model(Tweet)
    # If the user is in the home, it wont wanna seet his own retweets
    # Look for the retweets of the user and then get the tweets related to the them
    if is_retweet:
        retweets = Retweet.objects.filter(user=user).order_by('-created_at').select_related('tweet')
        tweets = Tweet.objects.filter(tweet_id__in=[retweet.tweet_id for retweet in retweets]).order_by('-created_at')
    # Look for the tweets that the user has liked it
    elif is_posts_liked:
        likes = Like.objects.filter(content_type=tweet_content_type, user=user).select_related('content_type')
        tweets = Tweet.objects.filter(tweet_id__in=[like.object_id for like in likes]).order_by('-created_at')
    # Get the tweets for the user_id or all tweets, ordered by the creation date
    else:
        tweets = Tweet.objects.filter(user_id=user_id).order_by('-created_at') if user_id else Tweet.objects.all().order_by('-created_at')
    # Get the user for the user_id or else use the user that is logged in
        user = User.objects.get(user_id=user_id) if user_id else user
    # Annotate tweets with comments count, retweet count, and like count
    tweets = tweets.annotate(
        comments_count=Count("comment"),
        retweet_count=Count("retweet"),
        like_count=Coalesce(
            Subquery(
                Like.objects.filter(
                    content_type=tweet_content_type,
                    object_id=OuterRef("tweet_id")
                ).values("object_id").annotate(count=Count("pk")).values("count")[:1]
            ),
            Value(0)
        ),
        id_like=Coalesce(
            Subquery(
                Like.objects.filter(
                    content_type=tweet_content_type,
                    object_id=OuterRef("pk"),
                    user=user
                ).values("like_id")[:1]
            ),
            Value(None)
        ),
    )

#web-1  | [22/Feb/2025 03:28:57] "GET /users/retweets/eaf18527-823f-4f87-ab27-002b8cb748da HTTP/1.1" 200 30970
#web-1  | [22/Feb/2025 03:29:30] "GET /users/retweets/eaf18527-823f-4f87-ab27-002b8cb748da HTTP/1.1" 200 30950


    # Convert tweets to list and add date_tmp attribute that will be used for sorting
    # and then make the diferentiation the actual date and the tweet/retweet date
    tweets = list(tweets)
    for tweet in tweets:
        tweet.date_tmp = tweet.created_at

    # Create a copy of tweets to avoid modifying the original list while iterating
    copy_tweets = copy.deepcopy(tweets)
    # If the user is looking for his retweets, then the tweets list will be empty
    if is_retweet:
        tweets = []
        for tweet in copy_tweets:
            retweets = Retweet.objects.filter(tweet=tweet, user=user).select_related('user')
            for retweet in retweets:
                tweet.user_id_reposter = retweet.user_id
                tweet.user_name_reposter = retweet.user.name
                tweet.date_tmp = retweet.created_at
                tweet.my_repost_id = retweet.retweet_id
                tweets.append(tweet)
    # Check if the tweet has been retweeted by the user and add retweet information
    # Doesnt matter if the tweets is reposted or no when it's checking  posts x likes
    if not is_posts_liked and is_in_home:
        for tweet in copy_tweets:
            retweets = Retweet.objects.filter(tweet=tweet).select_related('user')
            for retweet in retweets:
                tweet.user_id_reposter = retweet.user_id
                tweet.user_name_reposter = retweet.user.name
                tweet.date_tmp = retweet.created_at
                tweets.append(tweet)

    # Sort tweets by date_tmp in descending order
    sorted_tweet_data = sorted(tweets, key=lambda x: x.date_tmp, reverse=True)

    # Calculate delta_created for each tweet
    for tweet in sorted_tweet_data:
        tweet.delta_created = get_delta_created(tweet.date_tmp)

    # Serialize the sorted tweets
    return TweetSerializer(sorted_tweet_data, many=True)

def retrieve_information_unique_post(post_id=None):
    try:
        # Obtener el tweet basado en el post_id
        tweet = Tweet.objects.get(tweet_id=post_id)
        
        # Obtener el contenido tipo para el modelo Tweet
        tweet_content_type = ContentType.objects.get_for_model(Tweet)
        
        # Anotar el tweet con el conteo de comentarios, retweets y likes
        tweet.comments_count = Comment.objects.filter(tweet=tweet).count()
        tweet.retweet_count = Retweet.objects.filter(tweet=tweet).count()
        tweet.like_count = Like.objects.filter(content_type=tweet_content_type, object_id=tweet.tweet_id).count()
        
        # Obtener el like del usuario actual si existe
        user = tweet.user
        tweet.id_like = Like.objects.filter(content_type=tweet_content_type, object_id=tweet.tweet_id, user=user).values("like_id").first()
        
        # Calcular el delta de tiempo creado
        tweet.delta_created = get_delta_created(tweet.created_at)
        
        # Serializar el tweet
        return TweetSerializer([tweet], many=True)
    except Tweet.DoesNotExist:
        raise Exception("El tweet no existe")
    except Exception as e:
        raise Exception(f"Error al recuperar el tweet: {str(e)}")