import uuid
from django.db import models

class Like(models.Model):
    tweet_id = models.UUIDField(primary_key=True, default= uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class TypeLike(models.Model):
    tweet_id = models.AutoField(primary_key=True, max_digits= 1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
