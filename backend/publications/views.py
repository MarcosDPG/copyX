from django.contrib.contenttypes.models import ContentType
from django.db.models import Count, Subquery, OuterRef, Value
from django.db.models.functions import Coalesce
from django.utils import timezone

from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from interactions.models import Like

from .models import Tweet
from .serializers import TweetSerializer

@api_view(['GET','POST'])
def tweet_operations(request):
    if request.method == 'GET':
        try:
            # Get the content type for the Tweet model
            tweet_content_type = ContentType.objects.get_for_model(Tweet)
            # Count the comments, retweets and likes for each tweet
            tweets = Tweet.objects.annotate(
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
            # Calculate the time since the tweet was created
            for tweet in tweets:
                tweet.delta_created = format_timedelta(timezone.now() - tweet.created_at)
            # Serialize the tweets
            tweetSerializer = TweetSerializer(tweets, many=True)
            return Response(data=tweetSerializer.data)

        except Exception as e:
            return Response({"Error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    elif request.method == 'POST':
        tweetSerializer = TweetSerializer(data=request.data)
        if tweetSerializer.is_valid():
            tweetSerializer.save()
            return Response(tweetSerializer.data, status=status.HTTP_201_CREATED)
        return Response(tweetSerializer.errors,status=status.HTTP_400_BAD_REQUEST)

def format_timedelta(delta):
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