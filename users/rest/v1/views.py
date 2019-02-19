from rest_framework.viewsets import ReadOnlyModelViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework_extensions.mixins import DetailSerializerMixin

from users.models import User
from users.rest.v1.serializers import SimpleUserSerializer, DetailUserSerializer


class UsersViewSet(DetailSerializerMixin, ReadOnlyModelViewSet):
    """
    Пользователи системы
    """
    permission_classes = (IsAuthenticated,)
    serializer_class = SimpleUserSerializer
    serializer_detail_class = DetailUserSerializer

    def get_queryset(self):
        return User.objects.exclude(is_superuser=True)
