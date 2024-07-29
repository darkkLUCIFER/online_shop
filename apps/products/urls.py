from django.urls import path

from apps.products import views

app_name = 'products'

urlpatterns = [
    path('<slug:slug>/', views.ProductDetailView.as_view(), name='product_detail'),
]
