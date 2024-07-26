from auth_service.auth.views.user.urls import urlpatterns as user_urls

app_name = 'auth'


urlpatterns = []
urlpatterns += user_urls
