from rest_framework import routers

from users.rest.v1.views import UsersViewSet

router = routers.SimpleRouter()
router.register(r'users', UsersViewSet, basename='usr')

urlpatterns = [
]

urlpatterns += router.urls
