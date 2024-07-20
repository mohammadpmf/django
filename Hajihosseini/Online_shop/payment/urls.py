from django.urls import path

from . import views

app_name = 'payment'

urlpatterns = [
    # Hajihosseini links
    path('process/', views.payment_process_sandbox, name='payment_process'),
    path('callback/', views.payment_callback_sandbox, name='payment_callback'),

    # Zarinpal links
    path('request/', views.send_request, name='request'),
    path('verify/', views.verify , name='verify'),
]