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

from .models import Tweet, Retweet, Comment
from .serializers import TweetSerializer, RetweetSerializer, CommentSerializer

@api_view(['GET','POST'])
@authentication_classes([SessionAuthentication])
@permission_classes([IsAuthenticated])
def tweet_operations(request, user_id=None, postman=None):
    if request.method == 'GET':
        try:
            # Get the content type for the Tweet model
            tweet_content_type = ContentType.objects.get_for_model(Tweet)

            # Get the tweets for the user or all tweets, ordered by the creation date
            tweets = Tweet.objects.filter(user_id=user_id).order_by('-created_at') if user_id else Tweet.objects.all().order_by('-created_at')

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
                            user=request.user
                        ).values("like_id")[:1]
                    ),
                    Value(None)
                ),
            )

            # Convert tweets to list and add date_tmp attribute
            tweets = list(tweets)
            for tweet in tweets:
                tweet.date_tmp = tweet.created_at

            # Create a copy of tweets to avoid modifying the original list while iterating
            copy_tweets = copy.deepcopy(tweets)

            # Check if the tweet has been retweeted by the user and add retweet information
            for tweet in copy_tweets:
                retweets = Retweet.objects.filter(tweet=tweet).select_related('user')
                for retweet in retweets:
                    tweet.user_id_reposter = retweet.user_id
                    tweet.user_name_reposter = retweet.user.name
                    tweet.date_tmp = retweet.created_at
                    tweet.my_repost_id = retweet.retweet_id
                    tweets.append(tweet)

            # Sort tweets by date_tmp in descending order
            sorted_tweet_data = sorted(tweets, key=lambda x: x.date_tmp, reverse=True)

            # Calculate delta_created for each tweet
            for tweet in sorted_tweet_data:
                tweet.delta_created = get_delta_created(tweet.date_tmp)

            # Serialize the sorted tweets
            tweetSerializer = TweetSerializer(sorted_tweet_data, many=True)
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

@api_view(['GET','POST','DELETE'])
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
def comment_operations(request, comment_id=None):
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