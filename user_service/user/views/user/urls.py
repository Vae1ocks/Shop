from django.urls import path
from .views import *

urlpatterns = [
    path('detail/', GetUserInfoView.as_view()),
    path('edit-user/fn-pct/', EditUserNamePictureView.as_view()),
    path('edit-user/pass/', EditUserPasswordView.as_view()),
    # change email
    path('change-email/send-mail/', EditUserSendEmailView.as_view()),
    path('change-email/send-mail/confirm/', ConfirmEditUserEmailView.as_view()),
    path('change-email/send-mail/new-send/', SendMailNewEmailView.as_view()),
    path('change-email/send-mail/set-email/', SetNewEmailView.as_view()),
    # order history
    path('user/orders-history/', UserHistoryView.as_view()),

]
