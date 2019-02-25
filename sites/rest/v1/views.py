import django_filters.rest_framework
from rest_framework_extensions.mixins import DetailSerializerMixin

from rest_framework.viewsets import ReadOnlyModelViewSet, ModelViewSet
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.response import Response

from sites.models import Site, Article, UserArticle, UserSite
from sites.rest.v1.serializers import SimpleSiteSerializer, SimpleArticleSerializer, DetailArtileSerializer, \
    UserArticleSerializer, SimpleUserSiteSerializer, DetailUserSiteSerializer


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


class UserEstimationsViewSet(ModelViewSet):
    permission_classes = (IsAuthenticated,)
    serializer_class = UserArticleSerializer
    filter_backends = (django_filters.rest_framework.DjangoFilterBackend, )
    filter_fields = ('user', 'user_estimation', 'article')

    def get_queryset(self):
        return UserArticle.objects.all()


class UserSitesViewSet(ReadOnlyModelViewSet):
    """
    Предпочитаемые пользователем инфо ресурсы
    """
    permission_classes = (IsAuthenticated,)
    serializer_class = SimpleUserSiteSerializer

    def list(self, request, pk=None):
        """
        Список инфо ресурсов пользователя
        :param request:
        :param pk:
        :return:
        """
        queryset = UserSite.objects.filter(user__pk=pk)
        serializer = SimpleUserSiteSerializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None, interface_id=None):
        """
        Детальная информация, включая ключевые запросы пользователя
        :param request:
        :param pk:
        :param interface_id:
        :return:
        """
        queryset = UserSite.objects.filter(pk=interface_id).filter(user__pk=pk).last()
        serializer = DetailUserSiteSerializer(queryset, many=False)
        return Response(serializer.data)
