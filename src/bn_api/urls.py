from django.conf.urls import include, url

app_name = 'api'

urlpatterns = [
    url(r'v1/', include('bn_api.urls_api_v1')),
]
