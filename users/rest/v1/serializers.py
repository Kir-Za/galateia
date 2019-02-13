from django.contrib.auth import get_user_model

from rest_framework import serializers

from users.models import UserSite, UserArticle

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


class SimpleUserSiteSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserSite
        fields = ('pk', 'site',)
        read_only_fields = ('pk', 'site',)


class DetailUserSiteSerializer(serializers.ModelSerializer):
    key_words = serializers.ListField(source='get_key_words')
    exclude_words = serializers.ListField(source='get_exclude_words')

    class Meta:
        model = UserSite
        fields = ('pk', 'site', 'key_words', 'exclude_words')
        read_only_fields = ('pk', 'site', 'key_words', 'exclude_words')


class UserArticleSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserArticle
        fields = ('id', 'user', 'article', 'user_estimation')
