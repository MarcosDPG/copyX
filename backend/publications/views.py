from django.contrib.contenttypes.models import ContentType
from django.db.models import Count, Subquery, OuterRef, Value
from django.db.models.functions import Coalesce
from django.contrib.auth.decorators import login_required

from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from interactions.models import Like

from .models import Tweet
from .serializers import TweetSerializer

@api_view(['GET','POST'])
@login_required
def tweet_operations(request, user_id=None):
    if request.method == 'GET':
        try:
            # Get the content type for the Tweet model
            tweet_content_type = ContentType.objects.get_for_model(Tweet)
            # Count the comments, retweets and likes for each tweet
            tweets = Tweet.objects.filter(user_id=user_id) if user_id else Tweet.objects.all()
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
                        ).order_by().values("object_id").annotate(count=Count("pk")).values("count")[:1]
                    ),
                    # If the subquery returns NULL, it uses 0
                    Value(0)
                )
            )
            # Serialize the tweets
            tweetSerializer = TweetSerializer(tweets, many=True)
            return Response(data=tweetSerializer.data)

        except Exception as e:
            return Response({"Error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    elif request.method == 'POST':
        tweetSerializer = TweetSerializer(data=request.data, context={'request': request})
        if tweetSerializer.is_valid():
            tweetSerializer.save()
            return Response(tweetSerializer.data, status=status.HTTP_201_CREATED)
        return Response(tweetSerializer.errors,status=status.HTTP_400_BAD_REQUEST)

