from django.urls import path

from catalog import views


urlpatterns = [
    path('categories/', views.CategoriesListView.as_view(), name='categories_list'),
    path('catalog/', views.CatalogListView.as_view(), name='catalog_list'),
    path('products/popular/', views.PopularProductsListView.as_view(), name='popular_products_list'),
    path('products/limited/', views.LimitedProductsListView.as_view(), name='limited_products_list'),
    path('sales/', views.SalesListView.as_view(), name='sales_list'),
    path('banners/', views.BannersListView.as_view(), name='banners_list'),
    path('tags/', views.TagsListView.as_view(), name='tags_list'),
]
