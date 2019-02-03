from django.urls import path, include

from rest_framework.urlpatterns import format_suffix_patterns


urlpatterns = [
    path('', include('sites.urls')),
    path('users/', include('users.urls')),
    path('auth/', include('rest_auth.urls')),
]

urlpatterns = format_suffix_patterns(urlpatterns)
