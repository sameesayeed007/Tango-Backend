from django.urls import include, path
from . import views

urlpatterns = [
  
    #path('add/<int:productid>/<int:userid>/', views.add_to_cart),
    path('addcart/<int:productid>/', views.add_cart),
    path('increase/<int:productid>/', views.increase_quantity),
    path('decrease/<int:productid>/', views.decrease_quantity),
    path('delete/<int:productid>/', views.delete_product),
    path('checkout/', views.checkout),
    path('cart_view/', views.cart_view),
    path('cart_details/', views.cart_details),
    path('allorders/', views.all_orders),
    path('orders/', views.orders),
    path('orders_pending/', views.orders_pending),
    path('admin_approval/<int:order_id>', views.admin_approval),
    path('admin_cancellation/<int:order_id>', views.admin_cancellation),
    path('specific_order/<int:order_id>/', views.specific_order),
    path('orders_to_pay/', views.orders_to_pay),
    path('orders_to_ship/', views.orders_to_ship),
    path('orders_received/', views.orders_received),
    path('orders_cancelled/', views.orders_cancelled),
    path('cancel_order/', views.cancel_order),
    path('cancel_specific_order/<int:order_id>/', views.cancel_specific_order),
    path('cancel_cart/', views.cancel_cart),
    path('unpaidorders/', views.orders_not_paid),
    path('notdeliveredorders/', views.orders_not_delivered),
    path('deliveryinfo/', views.order_delivery),
    path('create_address/', views.create_address),
    path('show_address/', views.show_address),
    path('edit_address/', views.edit_address),
    path('check_coupon/', views.check_coupon),
    path('cancelorder/<int:order_id>/', views.cancelorder),
    path('order_info/<int:order_id>/', views.send_info),
    #path('addpoints/', views.add_points),
   

  
  

]