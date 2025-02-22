from django.contrib.auth.decorators import login_required
from django.contrib.contenttypes.models import ContentType
from django.db.models import Count, Subquery, OuterRef, Value
from django.db.models.functions import Coalesce
from django.shortcuts import render

import json

from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from interactions.models import Like

from .models import Tweet
from .serializers import TweetSerializer

@api_view(['GET','POST'])
@authentication_classes([SessionAuthentication])
@permission_classes([IsAuthenticated])
def tweet_operations(request, user_id=None):
    if request.method == 'GET':
        try:
            # Get the content type for the Tweet model
            tweet_content_type = ContentType.objects.get_for_model(Tweet)
            # Get the tweets for the user or all tweets, ordered by the creation date
            tweets = Tweet.objects.filter(user_id=user_id).order_by('-created_at') if user_id else Tweet.objects.all().order_by('-created_at')
            # Count the comments, retweets and likes for each tweet
            tweets = tweets.annotate(
                comments_count=Count("comment"),
                retweet_count=Count("retweet"),
                # Coallesce: If the subquery returns NULL, it uses 0
                like_count=Coalesce(
                    # Subquery: Get the count of likes for each tweet
                    Subquery(
                        Like.objects.filter(
                            # Filter by content type and tweet id
                            content_type=tweet_content_type,
                            object_id=OuterRef("tweet_id")
                        ).values("object_id").annotate(count=Count("pk")).values("count")[:1]
                    ),
                    # If the subquery returns NULL, it uses 0
                    Value(0)
                )
            )
            # Serialize the tweets
            tweetSerializer = TweetSerializer(tweets, many=True)
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