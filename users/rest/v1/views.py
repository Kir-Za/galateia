from django.shortcuts import get_object_or_404

from rest_framework.viewsets import ReadOnlyModelViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from users.models import User, UserSite
from users.rest.v1.serializers import SimpleUserSerializer, DetailUserSerializer, SimpleUserSiteSerializer, \
    DetailUserSiteSerializer


class UsersViewSet(ReadOnlyModelViewSet):
    """
    Пользователи системы
    """
    permission_classes = (IsAuthenticated,)

    def list(self, request, *args, **kwargs):
        """
        Список пользователей, включая не активных
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        queryset = User.objects.all()
        serializer = SimpleUserSerializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        """
        Детальная информация по каждому пользователю
        :param request:
        :param pk:
        :return:
        """
        queryset = User.objects.all()
        user = get_object_or_404(queryset, pk=pk)
        serializer = DetailUserSerializer(user)
        return Response(serializer.data)


class UserSitesViewSet(ReadOnlyModelViewSet):
    """
    Предпочитаемые пользователем инфо ресурсы
    """
    permission_classes = (IsAuthenticated,)

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
        queryset = UserSite.objects.filter(site__pk=site_id).filter(user__pk=pk).last()
        serializer = DetailUserSiteSerializer(queryset, many=False)
        return Response(serializer.data)
