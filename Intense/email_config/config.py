import requests
from django.urls import reverse,reverse_lazy
# from Intense import Integral_apis





EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_HOST_USER = 'fuhadfaizullah@gmail.com'
EMAIL_HOST_PASSWORD = 'faizullah1234567'
EMAIL_USE_TLS = True
EMAIL_USE_SSL = False

# val= Integral_apis.get_email_config()
# print(val)