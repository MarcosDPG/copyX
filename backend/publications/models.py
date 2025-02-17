import uuid
from django.db import models
from users.models import User

class Tweet(models.Model):
    tweet_id = models.UUIDField(primary_key=True, default= uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.CharField(max_length=300)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "Tweets"

class Retweet(models.Model):
    retweet_id = models.UUIDField(primary_key=True, default= uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    tweet = models.ForeignKey(Tweet, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "Retweets"

class Comment(models.Model):
    comment_id = models.UUIDField(primary_key=True, default= uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    tweet = models.ForeignKey(Tweet, on_delete=models.CASCADE)
    content = models.CharField(max_length=300)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "Comments"
