"""Tango URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from rest_framework.authtoken.views import obtain_auth_token 

#To show media files
from django.conf import settings
from django.contrib.staticfiles.urls import static, staticfiles_urlpatterns

urlpatterns = [
    path('admin/', admin.site.urls),
    path('ad/', include('Advertisement.urls')),
    path('impress/', include('Impression.urls')),
    path('site/', include('Site_settings.urls')),
    path('supports/', include('Support.urls')),
    path('email/', include('Emailing_Auth.urls')),
    path('Cart/', include('Cart.urls')),
    path('product/', include('Product.urls')),
    path('user/',include('User_details.urls')),
    path('productdetails/',include('Product_details.urls')),
    path('category/',include('Product_category.urls')),
]


urlpatterns += staticfiles_urlpatterns()
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)