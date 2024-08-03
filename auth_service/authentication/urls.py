from authentication.views.auth.urls import urlpatterns as auth_urls
from authentication.views.social.urls import urlpatterns as social_auth_urls
from authentication.views.another.urls import urlpatterns as another_urls

app_name = 'authentication'

urlpatterns = []

urlpatterns += auth_urls
urlpatterns += social_auth_urls
urlpatterns += another_urls