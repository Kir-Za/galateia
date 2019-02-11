import django_filters.rest_framework
from rest_framework_extensions.mixins import DetailSerializerMixin

from rest_framework.viewsets import ReadOnlyModelViewSet
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly

from sites.models import Site, Article
from sites.rest.v1.serializers import SimpleSiteSerializer, SimpleArticleSerializer, DetailArtileSerializer


class SitesListViewSet(ReadOnlyModelViewSet):
    """
    Список существующих целевых сайтов
    """
    permission_classes = (IsAuthenticatedOrReadOnly,)
    serializer_class = SimpleSiteSerializer
    filter_backends = (django_filters.rest_framework.DjangoFilterBackend,)
    filter_fields = ('is_active', )

    def get_queryset(self):
        return Site.objects.all()


class ArticlesViewSet(DetailSerializerMixin, ReadOnlyModelViewSet):
    """
    Существующие статьи.
    """
    permission_classes = (IsAuthenticatedOrReadOnly,)
    serializer_class = SimpleArticleSerializer
    serializer_detail_class = DetailArtileSerializer
    filter_backends = (django_filters.rest_framework.DjangoFilterBackend,)
    filter_fields = ('has_prices', 'has_percents', )

    def get_queryset(self):
        return Article.objects.all()
