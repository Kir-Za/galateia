from rest_framework import serializers

from sites.models import Site, Article


class SimpleSiteSerializer(serializers.ModelSerializer):
    """
    Новостной источник.
    """
    class Meta:
        model = Site
        fields = ('pk', 'target_url', 'is_active')
        read_only_fields = ('pk', 'target_url', 'is_active')


class SimpleArticleSerializer(serializers.ModelSerializer):
    """
    Список статей.
    """
    title = serializers.CharField(source='content.news_title')

    class Meta:
        model = Article
        fields = ('pk', 'link', 'title', 'has_prices', 'has_percents', 'frequent_words')
        read_only_fields = ('pk', 'link', 'title', 'has_prices', 'has_percents', 'frequent_words')


class DetailArtileSerializer(serializers.ModelSerializer):
    """
    Детальная информация по каждой статье, content может разниться в зависимости от сайта.
    """
    class Meta:
        model = Article
        fields = ('content', 'has_prices', 'has_percents', 'frequent_words')
        read_only_fields = ('content', 'has_prices', 'has_percents', 'frequent_words')
