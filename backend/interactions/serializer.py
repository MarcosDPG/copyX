from rest_framework import serializers
from .models import Like

class LikeSerializer(serializers.ModelSerializer):
    like_id = serializers.UUIDField(read_only=True)
    class Meta:
        model = Like
        fields = ["content_type","object_id","like_id"]
        extra_kwargs = {"content_type": {"write_only": True}, "object_id": {"write_only": True}}

    def get_like_id(self, obj):
        return obj.like_id