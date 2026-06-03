from django.urls import path
from . import views

urlpatterns = [
    path('initiate/', views.initiate_loan_payment),    # member starts payment
    path('verify/', views.verify_loan_payment),        # frontend verifies after redirect
    path('webhook/', views.paystack_webhook),          # Paystack calls this
    path('history/', views.payment_history),           # member views their payments
    path('admin/', views.admin_payment_list),          # admin views all payments
    path('<int:payment_id>/refund/', views.refund_payment),
]

