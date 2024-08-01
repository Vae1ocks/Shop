from user.views.user.urls import urlpatterns as auth_urls
from user.views.another.urls import urlpatterns as another_urls

app_name = 'user'

urlpatterns = []

urlpatterns += auth_urls

urlpatterns += another_urls