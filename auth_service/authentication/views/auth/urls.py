from django.urls import path

from .views import *


urlpatterns = [
    path('registration/', Registration.as_view(), name='registration'),
    path('confirm-registration/', ConfirmRegistration.as_view(),
         name='confirm-registration'),

    path('set-new-password/', SetNewPassword.as_view()),
    path('reset-password/send-mail/', ResetPassword.as_view()),
    path('reset-password/', ConfirmResetPassword.as_view()),

    path('login/', Login.as_view(), name='login'),
    path('logout/', Logout.as_view(), name='logout'),

    path('new-access-token/', GenerateAccessToken.as_view(), name='refresh-token'),
]
