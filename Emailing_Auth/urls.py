from django.urls import path
from .import views

app_name = 'Emailing_Auth'

urlpatterns = [
    path('', views.email_message),
    path('verification', views.email_verification),
    path('config_email', views.set_email_config),
    path('config_value', views.get_email_config_value, name = 'config_value'),
    path('all_config', views.show_all_email_config_value),
    path('update_config/<int:config_id>/', views.update_email_config),

]