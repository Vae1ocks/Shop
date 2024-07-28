from django.urls import path

from .views import *


urlpatterns = [
    path('registration/', Registration.as_view(), name='registration'),
    path('confirm-registration/<str:short_code>/', ConfirmRegistration.as_view(), name='confirm-registration'),
    path('login/', Login.as_view(), name='login'),
    path('logout/', Logout.as_view(), name='logout'),
    path('new-access-token/', GenerateAccessToken.as_view(), name='refresh-token'),
]
