import uuid
from django.db import models

class User(models.Model):
    user_id = models.UUIDField(primary_key=True, default= uuid.uuid4, editable=False)
    user_name = models.CharField(max_length=20, unique=True)
    name = models.CharField(max_length=30, blank= False)
    email = models.EmailField(max_length=50)
    password = models.CharField(max_length=64)
    birh_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)