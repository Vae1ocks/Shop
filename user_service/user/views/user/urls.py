from django.urls import path
from .views import *

urlpatterns = [
    path('<int:pk>/purchase-history', CategoriesBoughByUserView.as_view(),
         name='categories_bouth_by_user'),
    path('<int:pk>/representational-data/', UserRepresentationalView.as_view(),
         name='user_representational-data'),
    path('detail/', GetUserInfoView.as_view()),
    path('edit-user/fn-pct/', EditUserNamePictureView.as_view()),
    path('edit-user/pass/', EditUserPasswordView.as_view()),
    # change email
    path('change-email/send-mail/', EditUserSendEmailView.as_view()),
    path('change-email/send-mail/confirm/', ConfirmEditUserEmailView.as_view()),
    path('change-email/send-mail/new-send/', SendMailNewEmailView.as_view()),
    path('change-email/send-mail/set-email/', SetNewEmailView.as_view()),

]
