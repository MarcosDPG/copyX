from rest_framework import serializers

from .models import Tweet, Retweet, Comment

class TweetSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()
    user_id = serializers.SerializerMethodField(read_only=True)
    user_name = serializers.SerializerMethodField(read_only=True)
    delta_created = serializers.CharField(read_only=True)
    comments_count = serializers.IntegerField(read_only=True)
    like_count = serializers.IntegerField(read_only=True)
    retweet_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = Tweet
        fields = ["user","content","tweet_id","name","delta_created","comments_count","user_name","retweet_count","like_count","user_id"]
        read_only_fields = ["tweet_id", "name"]
        extra_kwargs = {
        'user': {'write_only': True}
        }


    def get_name(self, obj):
        return obj.user.name

    def get_user_name(self, obj):
        return obj.user.user_name

    def get_user_id(self, obj):
        return obj.user.user_id

class RetweetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Retweet
        fields = "__all__"

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = "__all__"
