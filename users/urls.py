from django.urls import path

from users.rest.v1.views import UsersViewSet, UserSitesViewSet


urlpatterns = [
    path('', UsersViewSet.as_view({'get': 'list'}), name='all_users'),
    path('<int:pk>/', UsersViewSet.as_view({'get': 'retrieve'}), name='detail_user'),
    path('<int:pk>/sites/', UserSitesViewSet.as_view({'get': 'list'}), name='all_prefer'),
    path('<int:pk>/sites/<int:site_id>/', UserSitesViewSet.as_view({'get': 'retrieve'}), name='detail_prefer'),
]
