from django.shortcuts import get_object_or_404
import django_filters.rest_framework

from rest_framework.viewsets import ReadOnlyModelViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from sites.models import Site, Article
from sites.rest.v1.serializers import SimpleSiteSerializer, SimpleArticleSerializer, DetailArtileSerializer


class SitesListViewSet(ReadOnlyModelViewSet):
    """
    Список существующих целевых сайтов
    """
    permission_classes = (IsAuthenticated,)
    serializer_class = SimpleSiteSerializer
    filter_backends = (django_filters.rest_framework.DjangoFilterBackend,)
    filter_fields = ('is_active', )

    def get_queryset(self):
        return Site.objects.all()


class ArticlesViewSet(ReadOnlyModelViewSet):
    """
    Существующие статьи
    """
    permission_classes = (IsAuthenticated,)


    def list(self, request, *args, **kwargs):
        """
        Саисок доступных статей
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        queryset = Article.objects.all()
        serializer = SimpleArticleSerializer(queryset, many=True)

        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        """
        Детальная информация по конкретной статье
        :param request:
        :param pk:
        :return:
        """
        queryset = Article.objects.all()
        article = get_object_or_404(queryset, pk=pk)
        serializer = DetailArtileSerializer(article)
        return Response(serializer.data)
