from rest_framework import serializers
from .models import Tweet, Retweet, Comment

class TweetSerializer(serializers.ModelSerializer):
    user_name = serializers.SerializerMethodField()
    delta_created = serializers.CharField(read_only=True)
    comments_count = serializers.IntegerField(read_only=True)
    like_count = serializers.IntegerField(read_only=True)
    retweet_count = serializers.IntegerField(read_only=True)
    user_id = serializers.UUIDField(read_only=True)
    id_like = serializers.CharField(read_only=True)
    user_id_reposter = serializers.UUIDField(read_only=True)
    user_name_reposter = serializers.CharField(read_only=True)
    
    class Meta:
        model = Tweet
        fields = ["content", "tweet_id", "user_name", "delta_created", "comments_count", "retweet_count",
                  "like_count", "user_id", "id_like", "user_id_reposter", "user_name_reposter"]
        read_only_fields = ["tweet_id", "user_id"]
        extra_kwargs = {"date_tmp": {"write_only": True}}

    def get_user_name(self, obj):
        return obj.user.name

    def create(self, validated_data):
        validated_data["user"] = self.context["request"].user
        return super().create(validated_data)

class RetweetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Retweet
        fields = ["tweet", "retweet_id"]
        extra_kwargs = {"tweet": {"write_only": True}}

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = "__all__"
