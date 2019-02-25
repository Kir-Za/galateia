from django.urls import path
from django.views.decorators.cache import cache_page

from rest_framework import routers

from sites.rest.v1.views import SitesListViewSet, ArticlesViewSet, UserEstimationsViewSet, UserSitesViewSet

router = routers.SimpleRouter()
router.register(r'estimations', UserEstimationsViewSet, basename='est')

urlpatterns = [
    path('sites/', SitesListViewSet.as_view({'get': 'list'}), name='list_sites'),
    path('articles/', cache_page(60*10)(ArticlesViewSet.as_view({'get': 'list'})), name='list_articles'),
    path('articles/<int:pk>/', ArticlesViewSet.as_view({'get': 'retrieve'}), name='detail_article'),
    path('users/<int:pk>/sites/', UserSitesViewSet.as_view({'get': 'list'}), name='list_prefer'),
    path('users/<int:pk>/sites/<int:interface_id>/', UserSitesViewSet.as_view({'get': 'retrieve'}),
         name='detail_prefer'),
]

urlpatterns += router.urls
