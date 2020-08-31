from django.urls import include, path
from . import views



urlpatterns = [

   path('add_ad/', views.add_ad),
   path('show_ad/<int:ad_id>/', views.show_ad),
   path('showallads/', views.show_all_ads),
   path('update/<int:ad_id>/', views.update_ad),
   path('delete/<int:ad_id>/', views.delete_ad),
  
]