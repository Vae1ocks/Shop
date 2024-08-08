from .views.chat.urls import urlpatterns as chat_urls
from .views.other.urls import urlpatterns as other_urls

app_name = 'chat'

urlpatterns = []

urlpatterns += chat_urls
urlpatterns += other_urls
