from django.shortcuts import get_object_or_404
import django_filters.rest_framework

from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_extensions.mixins import DetailSerializerMixin

from users.models import User, UserSite, UserArticle
from users.rest.v1.serializers import SimpleUserSerializer, DetailUserSerializer, SimpleUserSiteSerializer, \
    DetailUserSiteSerializer, UserArticleSerializer


class UsersViewSet(DetailSerializerMixin, ReadOnlyModelViewSet):
    """
    Пользователи системы
    """
    permission_classes = (IsAuthenticated,)
    serializer_class = SimpleUserSerializer
    serializer_detail_class = DetailUserSerializer

    def get_queryset(self):
        return User.objects.exclude(is_superuser=True)


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

    def retrieve(self, request, pk=None, site_id=None):
        """
        Детальная информация, включая ключевые запросы пользователя
        :param request:
        :param pk:
        :param site_id:
        :return:
        """
        queryset = UserSite.objects.filter(pk=site_id).filter(user__pk=pk).last()
        serializer = DetailUserSiteSerializer(queryset, many=False)
        return Response(serializer.data)


class UserEstimationsViewSet(ModelViewSet):
    permission_classes = (IsAuthenticated,)
    serializer_class = UserArticleSerializer
    filter_backends = (django_filters.rest_framework.DjangoFilterBackend, )
    filter_fields = ('user', 'user_estimation', 'article')

    def get_queryset(self):
        return UserArticle.objects.all()
