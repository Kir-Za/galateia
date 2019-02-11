from django.urls import path
from django.views.decorators.cache import cache_page

from sites.rest.v1.views import SitesListViewSet, ArticlesViewSet


urlpatterns = [
    path('sites/', SitesListViewSet.as_view({'get': 'list'}), name='all_sites'),
    path('articles/', cache_page(60*10)(ArticlesViewSet.as_view({'get': 'list'})), name='all_articles'),
    path('articles/<int:pk>/', ArticlesViewSet.as_view({'get': 'retrieve'}), name='detail_article'),
]
