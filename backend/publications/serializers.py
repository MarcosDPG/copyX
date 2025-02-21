from rest_framework import serializers
from django.utils import timezone
from .models import Tweet, Retweet, Comment
from users.models import User

class TweetSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()
    user_name = serializers.SerializerMethodField()
    delta_created = serializers.SerializerMethodField()
    comments_count = serializers.IntegerField(read_only=True)
    like_count = serializers.IntegerField(read_only=True)
    retweet_count = serializers.IntegerField(read_only=True)
    user_id = serializers.UUIDField(read_only=True)

    class Meta:
        model = Tweet
        fields = ["content", "name", "tweet_id", "user_name", "delta_created", "comments_count", "retweet_count", "like_count", "user_id"]
        read_only_fields = ["tweet_id", "user_id"]

    def get_user_name(self, obj):
        return obj.user.user_name
    
    def get_name(self, obj):
        return obj.user.name

    def get_delta_created(self, obj):
        delta = timezone.now() - obj.created_at
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

    def create(self, validated_data):
        validated_data["user"] = self.context["request"].user
        return super().create(validated_data)

class RetweetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Retweet
        fields = "__all__"

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = "__all__"
