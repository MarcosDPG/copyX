import uuid
from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from users.models import User

class Like(models.Model):
    tweet_id = models.UUIDField(primary_key=True, default= uuid.uuid4, editable=False)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    type_id = models.CharField()
    content = GenericForeignKey('content_type', "type_id")
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "Likes"

