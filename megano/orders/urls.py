from django.urls import path

from orders import views


urlpatterns = [
    path('orders', views.OrdersAPIView.as_view(), name='orders')
]