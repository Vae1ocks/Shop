from django.urls import path
from .views.store.urls import urlpatterns as store_urls

app_name = "store"

urlpatterns = []

urlpatterns += store_urls
