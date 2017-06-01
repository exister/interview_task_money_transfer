from bn_users.urls_api_v1 import urlpatterns as urlpatterns_users
from bn_accounts.urls_api_v1 import urlpatterns as urlpatterns_accounts


urlpatterns = []
urlpatterns += urlpatterns_users
urlpatterns += urlpatterns_accounts
