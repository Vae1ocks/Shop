from .views.favorites.urls import urlpatterns as favorites_urls
from .views.other.urls import urlpatterns as other_urls

app_name = "favorites"

urlpatterns = []

urlpatterns += favorites_urls
urlpatterns += other_urls
