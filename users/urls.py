from django.urls import path

from rest_framework import routers

from users.rest.v1.views import UsersViewSet, UserSitesViewSet, UserEstimationsViewSet

router = routers.SimpleRouter()
router.register(r'users', UsersViewSet, basename='usr')
router.register(r'estimations', UserEstimationsViewSet, basename='est')


urlpatterns = [
    path('users/<int:pk>/sites/', UserSitesViewSet.as_view({'get': 'list'}), name='list_prefer'),
    path('users/<int:pk>/sites/<int:site_id>/', UserSitesViewSet.as_view({'get': 'retrieve'}), name='detail_prefer'),
]

urlpatterns += router.urls
