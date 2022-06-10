from rest_framework import serializers
from . import models


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Post
        fields = (
            'id', 'content', 'owner', 'wall', 'pin_to_top', 
            'created_at', 'updated_at', 'reply_to', 'repost_of', 
        )
