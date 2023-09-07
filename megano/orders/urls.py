from django.urls import path

from orders import views


urlpatterns = [
    path('orders', views.OrdersAPIView.as_view(), name='orders'),
    path('order/<int:id>', views.OrderDetailsAPIView.as_view(), name='order_details'),
    path('payment/<int:id>', views.PaymentAPIView.as_view(), name='payment_user'),
]