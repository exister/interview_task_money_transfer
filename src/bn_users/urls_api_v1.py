from django.conf.urls import url

from .api.v1.users import UserViewSet


urlpatterns = [
    url('^users/$', UserViewSet.as_view({'get': 'list'}), name='users-list'),
    url('^users/(?P<pk>\d+)/$', UserViewSet.as_view({'get': 'retrieve'}), name='users-details'),
]
