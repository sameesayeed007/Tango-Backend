from django.urls import path, include
from .import views
from django.views.generic import TemplateView
from django.urls import path,include
from .views import RegisterView, SetNewPasswordAPIView, VerifyEmail, LoginAPIView, PasswordTokenCheckAPI, RequestPasswordResetEmail,MyTokenObtainPairView
from rest_framework_simplejwt.views import (
    TokenRefreshView,
)

urlpatterns = [
    
    path('register', RegisterView.as_view(), name="register"),
    path('login', LoginAPIView.as_view(), name="login"),
    path('email-verify', VerifyEmail.as_view(), name="email-verify"),
    path('token/refresh', TokenRefreshView.as_view(), name='token_refresh'),
    path('request-reset-email', RequestPasswordResetEmail.as_view(), name="request-reset-email"),
    path('password-reset/<uidb64>/<token>',PasswordTokenCheckAPI.as_view(), name='password-reset-confirm'),
    path('password-reset-complete', SetNewPasswordAPIView.as_view(), name='password-reset-complete'),
    path('guest_user/', views.insert_guest_user),
    path('insert_relation/', views.insert_user_relation),
    path('non_verified/<int:verified_user_id>', views.get_non_verified_user),
    path('verified/<int:non_verified_user_id>', views.get_verified_user),
    path('balance/', views.user_balace_value), # this url for balance
    path('add_wallet/', views.add_wallet_value), # this url for adding wallet value
    path('subtract_wallet/', views.subtract_wallet_value), # this url for subtracting wallet value
    path('point_add/', views.add_point), # this url for adding point value
    path('convert_point/',views.point_conversion), # this url for converting point values to currency
    path('get_profile/<int:user_id>', views.specific_user_profile), 
    path('create_profile/', views.create_specific_user_profile), 
    path('update_profile/<int:user_id>', views.update_user_profile), 
    path('delete_user/', views.user_delete), 
    path('user_balance/<int:user_id>', views.specific_user_balace_value), 
    path('user_signup/', views.user_signup), 
    path('user_credential/', views.user_credentials_retrive), 
    path('token/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('change_password/<int:user_id>/', views.user_password_change),

    
    
]
