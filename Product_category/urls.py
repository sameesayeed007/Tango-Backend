from django.urls import include, path
from . import views

app_name = 'Product_category'

urlpatterns = [
  
    path('insert/', views.insert_category),
    path('show/', views.products_section),
    path('allcategories/', views.allcategories),
    path('categories/', views.categories),
    path('subcategories/', views.sub_categories),

]