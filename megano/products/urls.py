from django.urls import path

from products import views


urlpatterns = [
    path('product/<int:pk>/', views.ProductDetailView.as_view(), name='products_details'),
    path('product/<int:pk>/reviews/', views.CreateReviewView.as_view(), name='create_review'),
]
