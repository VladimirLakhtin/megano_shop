from django.urls import path

from cart import views


urlpatterns = [
    path('basket', views.CartApiView.as_view(), name='basket'),
]
