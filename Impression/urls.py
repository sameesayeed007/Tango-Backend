from django.urls import path,include
from . import views

urlpatterns = [
    path('post_value/', views.insert_product_impression),
    path('get_specific/<int:product_id>/', views.get_specific_product_impression),
    path('delete_specific/<int:product_id>/', views.delete_specific_product_impression),
    path('get_user_impress/<int:product_id>/', views.get_impression_user_id),
    path('get_click_impress/<int:product_id>/', views.get_click_impression),
    path('get_view_impress/<int:product_id>/', views.get_view_impression),
    path('get_cart_impress/<int:product_id>/', views.get_cart_impression),
    path('get_sales_impress/<int:product_id>/', views.get_sales_impression),
    
]