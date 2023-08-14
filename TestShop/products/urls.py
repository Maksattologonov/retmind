from django.urls import path
from .views import ProductListAPIView, ProductsExportView

urlpatterns = [
    path('products/', ProductListAPIView.as_view(), name='get-product'),
    path('export/products/', ProductsExportView.as_view(), name='export-products'),
]
