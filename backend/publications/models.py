import uuid
from django.db import models

class Tweet(models.Model):
    tweet_id = models.UUIDField(primary_key=True, default= uuid.uuid4, editable=False)
    content = models.CharField(max_length=300)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Retweet(models.Model):
    tweet_id = models.UUIDField(primary_key=True, default= uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Comment(models.Model):
    tweet_id = models.UUIDField(primary_key=True, default= uuid.uuid4, editable=False)
    content = models.CharField(max_length=300)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
