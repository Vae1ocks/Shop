from django.urls import path

from .views import *


urlpatterns = [
    path('registration/', Registration.as_view()),
    path('confirm-registration/<str:short_code>/', ConfirmRegistration.as_view()),
    path('login/', Login.as_view()),
    path('logout/', Logout.as_view()),
    path('new-access-token/', GenerateAccessToken.as_view()),
]
