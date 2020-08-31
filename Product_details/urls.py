from django.urls import include, path
from . import views

app_name = 'Product_details'

urlpatterns = [
  
    path('addpoints/', views.add_points),
    path('updatepoints/<int:product_id>/', views.update_points),
    path('deletepoints/<int:product_id>/', views.delete_points),
    path('addprice/', views.add_price),
    path('updateprice/<int:product_id>/', views.update_price),
    path('deleteprice/<int:product_id>/', views.delete_price),
    path('addspec/', views.add_specification),
    path('updatespec/<int:product_id>/', views.update_specification),
    path('deletespec/<int:product_id>/', views.delete_specification),
    path('showspec/<int:product_id>/', views.show_specification,name='showspec'),
    path('show/<int:product_id>/', views.show),
    path('transfer/<int:user_id>/',views.transfer),
    path('detail/<int:product_id>/', views.product_detail),
  
    path('create_cupon/', views.insert_cupon),
    path('all_cupon/', views.get_all_cupons),
    path('update_cupon/<int:cupon_id>/', views.update_specific_cupons),
    path('delete_cupon/<int:cupon_id>/', views.delete_specific_cupons),

    path('all_discount/', views.get_all_discount_value), 
    path('specific_value/<int:product_id>/', views.get_update_specific_value),
    path('insert_specific/', views.insert_specific_discount_value),
    path('discount_delete/<int:product_id>/', views.delete_discount_value),
  
]