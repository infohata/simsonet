from rest_framework import serializers
from . import models


# class PostReplySerializer(serializers.ModelSerializer):
#     owner = serializers.ReadOnlyField(source='owner.username')
#     owner_id = serializers.ReadOnlyField(source='owner.id')

#     class Meta:
#         model = models.Post
#         fields = (
#             'id', 'content', 'owner', 'owner_id', 'pin_to_top', 
#             'created_at', 'updated_at',
#         )


class PostSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    owner_id = serializers.ReadOnlyField(source='owner.id')
    reply_to = serializers.ReadOnlyField(source='reply_to.id')
    reply_count = serializers.SerializerMethodField()
    replies = serializers.StringRelatedField(many=True)
    likes_count = serializers.SerializerMethodField()

    class Meta:
        model = models.Post
        fields = (
            'id', 'content', 'owner', 'owner_id', 'wall', 'pin_to_top', 
            'created_at', 'updated_at', 'reply_to', 'repost_of', 'replies', 
            'reply_count', 'likes_count',
        )

    def get_reply_count(self, obj):
        return models.Post.objects.filter(reply_to=obj).count()

    def get_likes_count(self, obj):
        return obj.likes.count()


class LikeSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    owner_id = serializers.ReadOnlyField(source='owner.id')
    post = serializers.ReadOnlyField(source='post.id')

    class Meta:
        model = models.Like
        fields = ('id', 'post', 'owner', 'owner_id', 'created_at')
