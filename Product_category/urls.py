from django.urls import include, path
from . import views

app_name = 'Product_category'

urlpatterns = [
  
    path('insert/', views.insert_category),
    path('show/<int:ids>/<str:level>/', views.products_section),
    path('allcategories/', views.allcategories),
    path('categories/', views.categories),
    path('subcategories/', views.sub_categories),
    path('subsubcategories/', views.sub_sub_categories),
    path('create_inventory_report/', views.insert_inventory_report),
    path('inventory_report/<int:product_id>/', views.get_inventory_report),

]