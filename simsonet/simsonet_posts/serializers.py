from rest_framework import serializers
from . import models


class PostSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    owner_id = serializers.ReadOnlyField(source='owner.id')

    class Meta:
        model = models.Post
        fields = (
            'id', 'content', 'owner', 'owner_id', 'wall', 'pin_to_top', 
            'created_at', 'updated_at', 'reply_to', 'repost_of', 
        )
