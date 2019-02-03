from rest_framework import serializers

from sites.models import Site, Article


class SimpleSiteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Site
        fields = ('pk', 'target_url', 'is_active')
        read_only_fields = ('pk', 'target_url', 'is_active')


class SimpleArticleSerializer(serializers.ModelSerializer):
    has_prices = serializers.BooleanField()
    has_percents = serializers.BooleanField()
    title = serializers.CharField(source='content.news_title')
    frequent_words = serializers.SerializerMethodField()

    class Meta:
        model = Article
        fields = ('pk','link', 'title', 'has_prices', 'has_percents', 'frequent_words')
        read_only_fields = ('pk', 'link', 'title', 'has_prices', 'has_percents', 'frequent_words')

    def get_frequent_words(self, obj):
        base_tuples = obj.get_frequent_words(number=5)
        return [i[1] for i in base_tuples]


class DetailArtileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = ('content', )
        read_only_fields = ('content', )
