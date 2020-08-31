from django.shortcuts import render, redirect
from django.template.loader import render_to_string,get_template
from django.core.mail import EmailMultiAlternatives, EmailMessage
from django.utils.html import strip_tags
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_text, DjangoUnicodeDecodeError
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.contrib.sites.shortcuts import get_current_site
from .serializers import EmailConfigSerializer
from Intense.models import EmailConfig
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
import requests
from django.core.mail import EmailMessage
from django.core.mail.backends.smtp import EmailBackend
from Intense.Integral_apis import get_email_config
from django.core.mail import *



def email_message(request):
    '''
        This method is for sending the message to the user through email. 
        For the better look this method can send email combined with any html template.

    '''
    #demo values
    values={
        'name' : 'fuhad',
        'email' : 'faizullahfuhad@gmail.com',
        'template' : 'email_template.html',
        'subject' : 'Thank you for purchasing',
        'sender' : 'fuhadfaizullah@gmail.com',
        'receiver': ['faizullahfuhad@gmail.com']
    }

    company={
        'name' : 'Company Name',
        'logo' : 'logo_img_src',
        'banner' : 'banner_img_src',
        'subject' : 'Thank you for purchasing',
        'sender' : 'fuhadfaizullah@gmail.com',
        'receiver': ['faizullahfuhad@gmail.com']
    }
    backend = EmailBackend(host='smtp.gmail.com', port=587, username='fuhadfaizullah@gmail.com', 
                       password='faizullah1234567', use_tls=True, fail_silently=False)

    # email = EmailMessage(subject='subj', body='body', from_email=from_email, to=to, 
    #          connection=backend)

    template = render_to_string (values['template'],{'name': values['name'], 'user_email': values['email'] })
    text_content = strip_tags(template)
    email = EmailMultiAlternatives(
        subject= values['subject'],
        body=text_content,
        from_email=values['sender'],
        to=values['receiver'],
        connection=backend
        )
    email.attach_alternative(template, "text/html")
    email.send()

    try:
        email.send()
        return render(request,'index.html')
    except:
        return render(request,'error.html',{'error': 'Internal server'})


def email_verification(request):
    '''
        This method is for sending the verification link to the user through email.
        Currently it sends link like https://127.0.0.1:8000 encrypted user id.

    '''
    #demo values
    user={
        'id': '1',
        'name' : 'fuhad',
        'template' : 'user_activation.html',
        'subject' : 'Activate your account',
        'sender' : 'fuhadfaizullah@gmail.com',
        'receiver': ['faizullahfuhad@gmail.com'],
        'status' : 'False',
        'current_site' : '127.0.0.1:8000'
    }

    company={
        'name' : 'Company Name',
        'logo' : 'logo_img_src',
        'banner' : 'banner_img_src',
        'subject' : 'Thank you for purchasing',
        'sender' : 'fuhadfaizullah@gmail.com',
        'receiver': ['faizullahfuhad@gmail.com']
    }
    config = get_email_config()
    # backend = EmailBackend(host='smtp.gmail.com', port=config['email_port'], username=config['email_host_user'],
    # password=config['email_host_password'], use_tls=config['Tls_value'],fail_silently=False)

    template = render_to_string (user['template'],{'name': user['name'], 'user_email': user['receiver'],'domain':user['current_site'], 'logo' : company['logo'], 'banner' : company['banner'], 'company_name' : company['name'], 
    'uid': urlsafe_base64_encode(force_bytes(user['id']))})
    text_content = strip_tags(template)


    email_message = EmailMultiAlternatives (
        user['subject'],
        text_content,
        user['sender'],
        user['receiver']
    )
    email_message.fail_silently=False 
    email_message.attach_alternative(template, "text/html")
    email_message.send()
    try:
        email_message.send()
        return render(request,'index.html')
    except:
        return render(request,'error.html',{'error': 'Internal server'})
    
   
@api_view (["GET", "POST"])
def set_email_config(request):

    if request.method == 'POST':
        print(request.data)
        email_config_value = EmailConfigSerializer (data= request.data)
        if(email_config_value.is_valid()):
            email_config_value.save()
            return Response (email_config_value.data, status=status.HTTP_201_CREATED)
        return Response (email_config_value.errors)



@api_view (["GET", "POST"])
def get_email_config_value(request):

    if request.method == 'GET':
        try:
            queryset = EmailConfig.objects.all().last()
            serializers = EmailConfigSerializer (queryset,many = False)
            return Response (serializers.data)
        except:
            return Response({'message': 'There is no information to display'})

@api_view (["GET", "POST"])
def show_all_email_config_value(request):

    if request.method == 'GET':
        try:
            queryset = EmailConfig.objects.all()
            serializers = EmailConfigSerializer (queryset,many = True)
            return Response (serializers.data)
        except:
            return Response({'message': 'There is no information to display'})

@api_view(['POST','GET'])
def update_email_config(request,config_id):
  
    try:
        queryset = EmailConfig.objects.get(pk = config_id)
    
    except :
        return Response({'message': 'This value does not exist'})

    if request.method == 'GET':
        serializers = EmailConfigSerializer (queryset,many = False)
        return Response (serializers.data)
 
    elif request.method == "POST" :
        try:
            serializers = EmailConfigSerializer (queryset, data= request.data)
            if(serializers.is_valid()):
                serializers.save()
                return Response (serializers.data, status=status.HTTP_201_CREATED)
            return Response (serializers.errors)
        except:
            return Response({'message': 'Information could not be updated'})
    
