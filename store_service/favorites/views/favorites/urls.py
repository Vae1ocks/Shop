from django.urls import path

from . import views

urlpatterns = [
    path('list/', views.FavoriteListView.as_view(), name='list'),
    path('create/', views.FavoriteCreateView.as_view(), name='create'),
    path('<int:pk>/delete/', views.FavoriteDeleteView.as_view(), name='delete'),
]