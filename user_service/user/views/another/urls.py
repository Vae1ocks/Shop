from django.urls import path
from .views import *


urlpatterns = [
    path('<int:pk>/purchase-history', CategoriesBoughByUserView.as_view(),
         name='categories_bought_by_user'),
    path('<int:pk>/representational-data/', UserRepresentationalView.as_view(),
         name='user_representational-data'),
    path('price-expectation/add/', AddPriceExpectation.as_view(),
         name='add_price_expectation'),
    path('price-expectation/remove/', RemovePriceExpectation.as_view(),
         name='remove_price_expectation'),
    path('price-expectation/detail/', DetailPriceExpectation.as_view(),
         name='detail_price_expectation')
]