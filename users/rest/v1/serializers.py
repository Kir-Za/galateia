from django.contrib.auth import get_user_model

from rest_framework import serializers

User = get_user_model()


class SimpleUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('pk', 'username', 'user_type')
        read_only_fields = ('pk', 'username', 'user_type')


class DetailUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('pk', 'username', 'first_name', 'last_name', 'email', 'is_active', )
        read_only_fields = ('pk', 'username', 'first_name', 'last_name', 'email', 'is_active', )
