from django.urls import path
from .views import *

urlpatterns = [
    path('<int:pk>/purchase-history', CategoriesBoughByUserView.as_view(),
         name='categories_bouth_by_user'),
    path('<int:pk>/representational-data/', UserRepresentationalView.as_view(),
         name='user_representational-data'),

]
