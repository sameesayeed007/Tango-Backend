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
    path('add_specification/<int:product_id>/', views.add_spec),
    #path('add_specification/<int:product_id>/', views.add_spec),
    path('edit_specification/<int:specification_id>/', views.edit_spec),
    path('delete_specification/<int:specification_id>/', views.delete_spec),
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
    # path('details_order/<int:order_id>/', views.get_product_lists),
    # path('confirm_order/', views.confirm_products),
    # path('inventory_lists/<int:order_details_id>/', views.get_inventory_lists),
    # path('subtract_quantity/<int:order_details_id>/', views.subtract_quantity),
    path('inventory_lists/<int:order_details_id>/',views.inventory_lists),
    path('admin_approval/<int:order_id>/', views.admin_approval),
    path('admin_cancellation/<int:order_id>/', views.admin_cancellation),
    path('available_colors/<int:product_id>/', views.color_size),
    path('available_sizes/<int:product_id>/', views.available_sizes),
    path('create_warehouse/', views.create_warehouse),
    path('create_shop/', views.create_shop),
    path('update_warehouse/<int:warehouse_id>/', views.update_warehouse),
    path('update_shop/<int:shop_id>/', views.update_shop),
    path('warehouses/', views.show_all_warehouses),
    path('shops/', views.show_all_shops),
    path('delete_warehouse/<int:warehouse_id>/', views.delete_warehouse),
    path('delete_shop/<int:shop_id>/', views.delete_shop),
    path('warehouse_products/<int:warehouse_id>/', views.warehouse_products),
    path('subtract_items/<int:order_details_id>/', views.subtract_items),
    path('item_cancellation/<int:order_details_id>/', views.item_cancellation),


    path('insert_quantity/', views.insert_product_quantity),
    path('shop_products/<int:shop_id>/', views.shop_products),
    # path('subtract_items/', views.subtract_items),

  
]