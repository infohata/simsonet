from django.contrib.auth import get_user_model
from rest_framework import serializers
from . import models


class ProfileSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')
    # picture = serializers.ImageField()

    class Meta:
        model = models.UserProfile
        fields = ('user', 'picture', )


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ('username', 'password', )
    
    def create(self, validated_data):
        password = validated_data.pop('password')
        user = get_user_model()(**validated_data)
        user.set_password(password)
        user.save()
        return user
