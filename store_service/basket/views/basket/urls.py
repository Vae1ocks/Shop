from django.urls import path
from .views import *


urlpatterns = [
    path('add/', BasketAddGoodsView.as_view(), name='basket_add_goods'),
    path('remove/', BasketRemoveGoodsView.as_view(), name='basket_remove_goods'),
    path('detail/', BasketDetailView.as_view(), name='basket_detail'),
]