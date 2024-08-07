from payment.views.payment.urls import urlpatterns as payment_views
from payment.views.other.urls import urlpatterns as other_views

app_name = 'payment'

urlpatterns = []

urlpatterns += payment_views
urlpatterns += other_views
