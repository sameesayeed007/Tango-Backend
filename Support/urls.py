from django.urls import include, path
from . import views

urlpatterns = [
  
  path('create_ticket/', views.create_ticket),
  path('create_reply/<int:ticket_id>/', views.create_reply),
  path('ticket_list/', views.ticket_list),
  path('edit_ticket/<int:ticket_id>/', views.edit_ticketinfo),
  path('specific_ticket/<int:ticket_id>/', views.specific_ticket),
  path('active_ticket/', views.active_ticket),
  path('sender_ticket/<int:sender_id>/', views.sender_ticket),
  path('receiver_ticket/<int:receiver_id>/', views.receiver_ticket),
  path('edit_reply/<int:reply_id>/', views.edit_ticketreply),
  path('delete_ticket/<int:ticket_id>/', views.delete_ticket),

]