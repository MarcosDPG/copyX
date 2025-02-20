import uuid

from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models

from users.models import User

class Like(models.Model):
    like_id = models.UUIDField(primary_key=True, default= uuid.uuid4, editable=False)
    # Save the content type of the object being liked (Tweet or Comment)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    # Save the ID of the object being liked (Tweet or Comment)
    object_id = models.UUIDField()
    # Create a generic foreign key to the object being liked, it means that the object being liked can be a Tweet or a Comment
    content_object = GenericForeignKey('content_type', 'object_id')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "Likes"

