from django.urls import path

from sites.rest.v1.views import SitesListViewSet, ArticlesViewSet


urlpatterns = [
    path('sites/', SitesListViewSet.as_view({'get': 'list'}), name='all_sites'),
    path('articles/', ArticlesViewSet.as_view({'get': 'list'}), name='all_articles'),
    path('articles/<int:pk>/', ArticlesViewSet.as_view({'get': 'retrieve'}), name='detail_article'),
]
