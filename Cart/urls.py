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
    path('allorders/', views.all_orders),
    path('orders_to_pay/', views.orders_to_pay),
    path('orders_to_ship/', views.orders_to_ship),
    path('orders_received/', views.orders_received),
    path('cancel_order/', views.cancel_order),
    path('cancel_specific_order/<int:order_id>/', views.cancel_specific_order),
    path('cancel_cart/', views.cancel_cart),
    path('unpaidorders/', views.orders_not_paid),
    path('notdeliveredorders/', views.orders_not_delivered),
    path('deliveryinfo/', views.order_delivery),
    path('create_address/', views.create_address),
    path('show_address/', views.show_address),
    path('edit_address/', views.edit_address),
    #path('addpoints/', views.add_points),
   

  
  

]