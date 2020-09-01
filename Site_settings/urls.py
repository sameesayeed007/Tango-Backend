from django.urls import path,include
from . import views

urlpatterns = [
    path('info/', views.CompanyInfos), # this url for company Info API
    path('update_info/', views.update_CompanyInfos), #*********
    path('delete_info/<int:info_id>/', views.delete_CompanyInfos), # this url is for specific roles update**
    path('banner/<int:banner_id>/', views.get_specific_Banners), # this url for Banner API
    path('banner_insert/', views.Banner_Insertion), 
    path('banner_value_update/<int:banner_id>', views.Banner_value_update), 
    path('banner_img_update/<int:banner_id>', views.Banner_image_add), 
    path('banner_img_delete/<int:banner_id>/<int:img_id>/', views.Banner_image_delete), 
    path('delete_banner/<int:banner_id>', views.delete_Banner), # this url is fto delete banner
    path('roles/', views.All_Roles), # this url for Roles and Permissions API
    path('specific_roles/<int:roles_id>/', views.Specific_Roles), # this url is for specific roles update
    path('delete_role/<int:role_id>/', views.delete_Roles), # this url is for specific roles update***
    path('currency/', views.Currency_value), # this url is for currency value
    path('last_currency/', views.latest_Currency_value), # this url is for getting latest currency value***
    path('specific_currency/<int:currency_id>', views.Specific_Currency_get_delete), # this url is for getting a specific currency
    path('theme/', views.all_theme_infos), # this url is for Themes
    path('specific_theme/<int:theme_id>', views.Specific_theme), # this url is for getting a specific theme
    path('theme_delete/<int:theme_id>', views.delete_theme), # this url is for deleting theme
    path('Api/', views.all_APIs_infos), # this url is for API infos
    path('specific_Api/<int:Api_id>', views.Specific_Api), # this url is for getting a specific Api
    path('Api_delete/<int:Api_id>', views.delete_Api), # this url is for deleting Api
    path('settings/', views.site_all_settings), # this url is for setting table
    path('update_setting/<int:setting_id>', views.settings_update), # this url is for setting update
    path('insert_faq/', views.Faq_insertion),
    path('show_faq/', views.show_all_Faq),
    path('specific_faq/<int:faq_id>/', views.specific_faq),
    path('delete_faq/<int:faq_id>/', views.delete_specific_faq),
    path('contact/', views.insert_contact),
    path('all_contact/', views.get_all_contact),
    path('delete_contact/<int:contact_id>/', views.delete_specific_contactUs),
    path('unattend_contact/', views.get_all_unattended_contact),
    path('attended_contact/<int:contact_id>/', views.admin_attend_contact),
    
    

]