from django.urls import path
from . import views

urlpatterns = [
    # Main SPA Entry Point
    path('', views.vue_app, name='home'),
    
    # API Endpoints
    path('api/products/', views.api_product_list, name='api_product_list'),
    path('api/products/<int:pk>/', views.api_product_detail, name='api_product_detail'),
    path('api/metadata/', views.api_metadata, name='api_metadata'),
]
