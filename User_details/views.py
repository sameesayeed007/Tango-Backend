from django.shortcuts import render , redirect
from rest_framework import generics, status, views
from .serializers import RegisterSerializer, RelationSerializer,SetNewPasswordSerializer, UserBalanceSerializer, ResetPasswordEmailRequestSerializer, EmailVerificationSerializer,UserRelationSerializer, LoginSerializer,MyTokenObtainPairSerializer , UserSerializer , ProfileSerializer,GuestUserSerializer,UserSerializerz,GuestSerializer
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from Intense.models import User , user_relation,Settings,user_balance
from django.contrib.auth import authenticate

from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
import jwt
from django.conf import settings
from rest_framework.decorators import api_view
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.encoding import smart_str, force_str, smart_bytes, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse

from django.contrib import auth
from django.conf import settings
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework import permissions, status
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView, RetrieveAPIView, CreateAPIView, GenericAPIView , UpdateAPIView 
from .utils import Util   
from rest_framework.exceptions import PermissionDenied, NotAcceptable, ValidationError

from django.views.decorators.debug import sensitive_post_parameters
from django.utils.decorators import method_decorator
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
from Intense.models import Profile, User , user_relation,Guest_user

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from .decorators import unauthenticated_user, allowed_users, admin_only
from django.contrib import messages
from django.db import transaction
from Intense.Integral_apis import create_user_balance,create_user_profile
# from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from django.contrib.auth.hashers import make_password


class RegisterView(generics.GenericAPIView):
    '''
    This is for user Registration. User registration and verification will be performed using email.
    '''

    serializer_class = RegisterSerializer

    def post(self, request):
        user = request.data
        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        user_data = serializer.data
        user = User.objects.get(email=user_data['email'])
        token = RefreshToken.for_user(user).access_token
        current_site = get_current_site(request).domain
        relativeLink = reverse('email-verify')
        absurl = 'http://'+current_site+relativeLink+"?token="+str(token)
        email_body = 'Hi '+user.username + \
            '\n Use the link below to verify your email \n' + absurl
        data = {'email_body': email_body, 'to_email': user.email,
                'email_subject': 'Verify your email'}

        Util.send_email(data)
        return Response({'success': 'A verification link has been sent to your email'}, status=status.HTTP_201_CREATED)


class VerifyEmail(views.APIView):
    '''
    This is email verification API.
    '''
    serializer_class = EmailVerificationSerializer

    def get(self, request):
        token = request.GET.get('token')
        try:
            payload = jwt.decode(token, settings.SECRET_KEY)
            user = User.objects.get(id=payload['user_id'])
            if not user.is_verified:
                user.is_verified = True
                user.save()
            balance_values = {'user_id':payload['user_id']}
            create_user_balance(balance_values)
            profile_values ={'user_id':payload['user_id'],'email':user.email}
            create_user_profile(profile_values)
            
            return Response({'email': 'Successfully activated'}, status=status.HTTP_200_OK)
        except jwt.ExpiredSignatureError as identifier:
            return Response({'error': 'Activation Expired'}, status=status.HTTP_400_BAD_REQUEST)
        except jwt.exceptions.DecodeError as identifier:
            return Response({'error': 'Invalid token'}, status=status.HTTP_400_BAD_REQUEST)



@api_view (["GET", "POST"])
def dummy_user_signup(request):
    '''
    This is for user signup without Email varification. User will be able to signup using email and password. Signup will automatically create
    corresponding user profile and balance. Calling http://127.0.0.1:8000/user/user_signup/ will cause to invoke this Api.
    Response Type : Post
    Required filed: email, password
    Successful Post response:
        {
            "success": true,
            "message": "A verification link has been sent to your email"
        }
    unsuccessful Post Response:
        {
            "success": false,
            "message": "Some internal problem occurs"
        }
    '''
    if request.method == 'POST':
        try:
            serializer_class = RegisterSerializer
            user = request.data
            serializer = serializer_class(data=user)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            user_data = serializer.data
            user = User.objects.get(email=user_data['email'])
            if not user.is_verified:
                user.is_verified = True
                user.save()
            balance_values = {'user_id':user.id}
            create_user_balance(balance_values)
            profile_values ={'user_id':user.id,'email':user.email}
            create_user_profile(profile_values)
            return Response(
                {
                'success': True,
                'message': 'You have been registered'
                },
                status=status.HTTP_201_CREATED
                )
        except:
            return Response(
                {
                'success': False,
                'message': 'Some internal problem occurs'
                }
                
                )



@api_view (["POST",])
def dummy_login(request):



    data = request.data
    print(request.data)
    email = data['email']
    password = data['password']
    user = authenticate(email=email, password=password)
    

    if user:

        request.session['user_id'] = user.id
        request.session['user_email'] = user.email
        


        return Response(
        {
        'success': True,
        'message': 'You have been logged in',
        'user' : {'user_email': user.email,'user_id': user.id,'role':user.role}
        
        })


    else:


        return Response(
        {
        'success': False,
        'message': 'You have entered the wrong username or password'
        })


@api_view (["POST",])
def dummy_logout(request):
    try:
        del request.session['user_id']
        del request.session['user_email']
        return Response(
        {
        'success': True,
        'message': 'You have been logged out'
       
        })
    except KeyError:

        return Response(
        {
        'success': False,
        'message': 'You are already logged out'
       
        })




#This is for the admin panel.Admin will use this to create a user
@api_view (["POST",])
def create_user(request):

    email = request.data.get('email')
    password = request.data.get('password')
    role = request.data.get('role')
    pwd = make_password(password)
    username = request.data.get('username')
    phone_number = request.data.get('phone_number')
    if username is None:
        username = ""
    if phone_number is None:
        phone_number = ""
    



    #Create an user 
    if role == "Admin" or "Staff":

        new_user = User.objects.create(email=email,password=pwd,pwd=password,role=role,is_staff=True,is_verified=True,is_active=True,username=username,phone_number=phone_number)
        new_user.save()
        user_id = new_user.id
        email = new_user.email
        print(new_user)
        data = {'email':email,'password':pwd,'pwd':password,'role':role,'is_staff':True,'is_verified':True,'is_active':True,'username':username,'phone_number':phone_number}
        new_serializer = UserSerializerz(new_user,data=data)

        if new_serializer.is_valid():
            new_serializer.save()
        
            balance_values = {'user_id':user_id}
            create_user_balance(balance_values)
            profile_values ={'user_id':user_id,'email':email}
            create_user_profile(profile_values)
            data = new_serializer.data

        # try:
        #     current_user = User.objects.get(id=user_id)
        # except:
        #     current_user = None

        # if current_user:
        #     new_serializer = UserSerializerz(new_user,many=False)
        #     data = new_serializer.data
        # else:
        #     data = {}

            return Response(
            {
            'success': True,
            'message': 'User has been created',
            'data' : data,
            # 'encrypted_password': data["password"],
            'password': password
           
            })

        else:
            print(new_serializer.errors)
            return Response(
            {
            'success': False,
            'message': 'Could not create user',
            
           
            })

        
    elif role == "Seller":

        new_user = User.objects.create(email=email,pwd=password,password=pwd,role=role,is_suplier=True,is_staff=True,is_verified=True,is_active=True,username=username,phone_number=phone_number)
        new_user.save()
        user_id = new_user.id
        email = new_user.email
        data = {'email':email,'password':pwd,'pwd':password,'role':role,'is_staff':True,'is_verified':True,'is_active':True,'is_suplier':True,'username':username,'phone_number':phone_number}

        new_serializer = UserSerializerz(new_user,data=data)
        if new_serializer.is_valid():
            new_serializer.save()
            balance_values = {'user_id':user_id}
            create_user_balance(balance_values)
            profile_values ={'user_id':user_id,'email':email}
            create_user_profile(profile_values)
            data = new_serializer.data
        # try:
        #     current_user = User.objects.get(id=user_id)
        # except:
        #     current_user = None

        # if current_user:
        #     new_serializer = UserSerializerz(new_user,many=False)
        #     data = new_serializer.data
        # else:
        #     data = {}

            return Response(
            {
            'success': True,
            'message': 'User has been created',
            'data' : data,
            'password':password
           
            })

        else:
            print(new_serializer.errors)
            return Response(
            {
            'success': False,
            'message': 'Could not create user',
            
           
            })

        

    else:

        return Response(
            {
            'success': False,
            'message': 'Insert the correct role'
           
            })





@api_view (["POST",])
def update_user(request,user_id):


    print(request.data)


    try:
   
        users = User.objects.get(id=user_id)


    except:

        users = None


    if users:

        user_serializer = UserSerializerz(users,data=request.data)
        print(user_serializer.is_valid())
        if user_serializer.is_valid():
            print("ashterse")
            user_serializer.save()
            return Response(            {
            'success': True,
            'message': 'User details have been updated',
            'data': user_serializer.data
           
            })

        else:
            print(user_serializer.errors)
            return Response(            {
            'success': False,
            'message': 'User details could not be updated',
            'data': {}
           
            })

    else:

        return Response(            {
            'success': False,
            'message': 'This user does not exist',
            'data': {}
           
            })








@api_view (["GET",])
def show_users(request):

    try:

        users = User.objects.filter(role="Admin")|User.objects.filter(role="Staff")|User.objects.filter(role="Seller")

    except:

        users = None

    if users:

        user_serializer = UserSerializerz(users,many=True)

        return Response(
            {
            'success': True,
            'message': 'User details is shown',
            'data': user_serializer.data
           
            })


    else:


        return Response(
            {
            'success': False,
            'message': 'User details is not shown',
            'data': {}
           
            })




@api_view (["GET",])
def get_client_ip(request):
    user_data = {'non_verified_user_id':-1 , 'ip_address':""}
    if 'HTTP_X_FORWARDED_FOR' in request.META:
        print("astese2")
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        ip = x_forwarded_for.split(',')[0]

        try:

            guest_user = Guest_user.objects.get(ip_address=ip)
        except:

            guest_user = None

        if guest_user is None:
            #Create a guest_user
            g_user = Guest_user.objects.create(ip_address=ip)
            g_user.save()


            guest_serializer = GuestSerializer(g_user,data=request.data)
            if guest_serializer.is_valid():
                guest_serializer.save()
                ip_addr = guest_serializer.data['id']
                ip_address_no = guest_serializer.data['ip_address']

                non_verified_user_id = ip_addr
                ip_address = ip_address_no
                # Inserting the user into the user relation table
                data = {'non_verified_user_id': non_verified_user_id}
                #relation = user_relation.objects.create(non_verified_user_id=non_verified_user_id)
                relation = RelationSerializer(data=data)
                if relation.is_valid():
                    relation.save()




            else:
                ip_address = ""
                non_verified_user_id = -1
                
               

        else:
            
            non_verified_user_id = guest_user.non_verified_user_id
            ip_address = guest_user.ip_address



        user_data = {'success':True,'non_verified_user_id': non_verified_user_id}
    else:
        
        ip = request.META.get('REMOTE_ADDR')
        #checking to see if the guest user already exists
        #ip = '121.0.0.1'
        try:
            guest_user = Guest_user.objects.get(ip_address=ip)
        except:
            guest_user = None
        if guest_user is None:
            #Create a guest_user
            g_user = Guest_user.objects.create(ip_address=ip)
            g_user.save()


            guest_serializer = GuestSerializer(g_user,data=request.data)
            if guest_serializer.is_valid():
                guest_serializer.save()
                ip_addr = guest_serializer.data['id']
                ip_address_no = guest_serializer.data['ip_address']

                non_verified_user_id = ip_addr
                ip_address = ip_address_no
                # Inserting the user into the user relation table
                data = {'non_verified_user_id': non_verified_user_id}
                #relation = user_relation.objects.create(non_verified_user_id=non_verified_user_id)
                relation = RelationSerializer(data=data)
                if relation.is_valid():
                    relation.save()




            else:
                ip_address = ""
                non_verified_user_id = -1
                
               

        else:
            
            non_verified_user_id = guest_user.non_verified_user_id
            ip_address = guest_user.ip_address



        user_data = {'success':True,'non_verified_user_id': non_verified_user_id}




    return Response(user_data)








        




    










@api_view (["GET", "POST"])
def user_signup(request):
    '''
    This is for user signup without Email varification. User will be able to signup using email and password. Signup will automatically create
    corresponding user profile and balance. Calling http://127.0.0.1:8000/user/user_signup/ will cause to invoke this Api.
    Response Type : Post
    Required filed: email, password
    Successful Post response:
        {
            "success": true,
            "message": "A verification link has been sent to your email"
        }
    unsuccessful Post Response:
        {
            "success": false,
            "message": "Some internal problem occurs"
        }
    '''
    if request.method == 'POST':
        try:
            serializer_class = RegisterSerializer
            user = request.data
            serializer = serializer_class(data=user)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            user_data = serializer.data
            user = User.objects.get(email=user_data['email'])
            if not user.is_verified:
                user.is_verified = True
                user.save()
            balance_values = {'user_id':user.id}
            create_user_balance(balance_values)
            profile_values ={'user_id':user.id,'email':user.email}
            create_user_profile(profile_values)
            return Response(
                {
                'success': True,
                'message': 'A verification link has been sent to your email'
                },
                status=status.HTTP_201_CREATED
                )
        except:
            return Response(
                {
                'success': False,
                'message': 'Some internal problem occurs'
                }
                
                )
@api_view (["GET", "POST"])
def user_password_change (request,user_id):
    try: 
        user_profile = Profile.objects.get(user_id = user_id)
        user= User.objects.get(id = user_id)
    except :
        return Response({
            'success': False,
            'message': 'User does not exist'
            })

    if(request.method == "POST"):
        email = user_profile.email
        old_password = request.data['old_password']
        new_password = request.data['new_password']
        confirm_password = request.data['confirm_password']

        user = auth.authenticate(email=email, password=old_password)
        if not user:
            return Response({
                'success': False,
                'message': 'User credential is invalid'
                })
        else:
            if new_password==confirm_password:
                user.set_password(new_password)
                user.save()
                return Response ({
                        'success': True,
                        'message': 'Password has been changed successfully'
                    }, status=status.HTTP_201_CREATED)
            else:
                 return Response ({
                    'success': False,
                    'message': 'New password and Confirm password did not match',
                })



@api_view (["GET", "POST"])
def user_credentials_retrive (request):
    '''
    This method will give detail user information upon getting the token in header as named Authorization. 
    Url: http://127.0.0.1:8000/user/user_credential
    Response type : get
    Required : token in header as bellow format
        'Authorization' : 'Token'
    Successful get Response:
        {
            "success": true,
            "user": {
                "id": 8,
                "name": null,
                "email": "abcdef@gmail.com",
                "profile_picture": null,
                "phone_number": null,
                "gender": "",
                "city": null,
                "district": null,
                "road_number": null,
                "building_number": null,
                "apartment_number": null,
                "user_id": 12
            }
        }
    Unsuccessful get response:
        {
            "success": false,
            "user": ""
        }
    '''
    if request.method == 'GET':
        #value = "Token eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTU5OTA1Mjg5NSwianRpIjoiMjMxZjU0NTc4Y2FlNDFmNDk5NDc1ZGNmZmFmN2U3NmQiLCJ1c2VyX2lkIjoyfQ.ygudAXnaafE_Tq82CsVrSKt1YLsuIZ4bCAOsZ9a7j5Q"
        try:
            # print("ashche")
            # encoded_token = jwt.encode({'user_id': 'abc'}, settings.SECRET_KEY, algorithm='HS256')
            # print(encoded_token)
            # val=jwt.decode(encoded_token, settings.SECRET_KEY, algorithms=['HS256'])
            # print(val)
            token = request.headers['Authorization']
            TokenArray = token.split(" ")
            #token = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNTk5MTA0NTEwLCJqdGkiOiJiMzQ4NWVhNmVjOTU0M2I4ODRhMzM5MDZiNjg3ZWMyOCIsInVzZXJfaWQiOjJ9.LQQMqXD8Qo5Pnaa0Oqh7sL9X4KuByqh32K4djfU-BQA"
            # print("++++++++++++++++++++++++++++++")
            # print(token)
            #print(settings.SECRET_KEY)
            payload = jwt.decode(TokenArray[1], settings.SECRET_KEY)
            user_id = payload['user_id']
            user_profile = Profile.objects.get(user_id = user_id)
            user_profile_serializer = ProfileSerializer (user_profile, many = False)
            return Response ({
                'success': True,
                'user': user_profile_serializer.data
                    },status=status.HTTP_204_NO_CONTENT
                )
        except:
             return Response ({
                'success': False,
                'user': ''
                 })

class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer

@api_view (["GET","POST"])
def user_delete(request):
   
    users = User.objects.all()
    profile_data = Profile.objects.all()
    if request.method == "POST":
        try:
            users.delete()
            profile_data.delete()
            return Response({'message': 'Users are deleted successfully!'}, status=status.HTTP_204_NO_CONTENT)
        except:
            return Response ({'message': 'There is no value'})



@api_view (["GET","POST"])
def delete_user(request,user_id):

    try:
   
        users = User.objects.get(id=user_id)


    except:

        users = None


    if users:
        users.delete()
        return Response ({
                'success': True,
                'message': 'The user has been deleted'
                 })
    else:

        return Response ({
                'success': False,
                'message': 'The user down not exist'
                 })














class LoginAPIView(generics.GenericAPIView):
    '''
    This is user Login Api.
    '''
    serializer_class = LoginSerializer

    def post(self, request):
        print(request.data['email'])
        user = User.objects.get(email=request.data['email'])
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class RequestPasswordResetEmail(generics.GenericAPIView):
    '''
    This block of code is for requesting to reset password.
    '''
    serializer_class = ResetPasswordEmailRequestSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)

        email = request.data['email']

        if User.objects.filter(email=email).exists():
            user = User.objects.get(email=email)
            uidb64 = urlsafe_base64_encode(smart_bytes(user.id))
            token = PasswordResetTokenGenerator().make_token(user)
            current_site = get_current_site(
                request=request).domain
            relativeLink = reverse(
                'password-reset-confirm', kwargs={'uidb64': uidb64, 'token': token})
            absurl = 'http://'+current_site + relativeLink
            email_body = 'Hello, \n Use link below to reset your password  \n' + absurl
            data = {'email_body': email_body, 'to_email': user.email,
                    'email_subject': 'Reset your passsword'}
            Util.send_email(data)
        return Response({'success': 'We have sent you a link to reset your password'}, status=status.HTTP_200_OK)


class PasswordTokenCheckAPI(generics.GenericAPIView):
    '''
    This will generate token for password.
    '''
    serializer_class = SetNewPasswordSerializer

    def get(self, request, uidb64, token):

        try:
            id = smart_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(id=id)

            if not PasswordResetTokenGenerator().check_token(user, token):
                return Response({'error': 'Token is not valid, please request a new one'}, status=status.HTTP_401_UNAUTHORIZED)

            return Response({'success': True, 'message': 'Credentials Valid', 'uidb64': uidb64, 'token': token}, status=status.HTTP_200_OK)

        except DjangoUnicodeDecodeError as identifier:
            #if not PasswordResetTokenGenerator().check_token(user):
            return Response({'error': 'Token is not valid, please request a new one'}, status=status.HTTP_401_UNAUTHORIZED)


class SetNewPasswordAPIView(generics.GenericAPIView):
    '''
    This block of setting new password.
    '''
    serializer_class = SetNewPasswordSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response({'success': True, 'message': 'Password reset success'}, status=status.HTTP_200_OK)



class ProfileAPIView(APIView):
    # permission_classes = [auth.authenticate]

    def get(self, request, pk):
        profile = Profile.objects.get(pk=pk)
        serializer = ProfileSerializer(profile, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)

@api_view (["GET","POST"])
def create_specific_user_profile(request):
    '''
    This is for creating user profile. It will be created automatically after creating user account.
    '''
    if request.method == 'POST':
        user_profile = ProfileSerializer (data= request.data)
        if(user_profile.is_valid()):
            user_profile.save()
            return Response (user_profile.data, status=status.HTTP_201_CREATED)
        return Response (user_profile.errors)


@api_view (["GET","POST"])
def specific_user_profile(request, user_id):
    '''
    This is for getting specific profile data.
    '''

    if request.method == 'GET':
        #print(request.META['HTTP_HOST'])
       
        try:

            user_profile = Profile.objects.get(user_id = user_id)

        except:

            user_profile = None

        print(user_profile)
        if user_profile:

            user_profile_serializer = ProfileSerializer (user_profile, many = False)
            return Response ({'success':True,'message':'Data is shown','data':user_profile_serializer.data})
        else:
            return Response({'success':True,'message':'Data is shown','data':{}})

@api_view (["GET","POST"])
def update_user_profile(request,user_id):
    '''
    This api is for updating a particular user profile.
    '''

    try: 
        user_profile = Profile.objects.get(user_id = user_id)
    except :
        return Response({'message': 'User profile does not exist'})

    if(request.method == "GET"):
        user_profile_serializer = ProfileSerializer (user_profile, many = False)
        return Response (user_profile_serializer.data)

    elif(request.method == "POST"):
        user_profile = ProfileSerializer (user_profile, data= request.data)
        if(user_profile.is_valid()):
            user_profile.save()
            return Response (user_profile.data, status=status.HTTP_201_CREATED)
        return Response (user_profile.errors)
        




@api_view (["GET","POST"])
def insert_guest_user(request):
    '''
    This is for guest user. All the guest user id will be stored here and corresponding guest user ip there will be an id which will be sent to front end 
    for storing. Calling http://127.0.0.1:8000/user/guest_user/ will cause to invoke this Api. There is only post api.

    Post Api Response :
        ip_address : (This is a character filed. Here the ip address of the guest user must need to be sent.)
    '''
    values ={'ip_address' : '127.01.10.23'}

    if request.method == 'POST':
        guest_user_serializer = GuestUserSerializer (data= values)
        if(guest_user_serializer.is_valid()):
            guest_user_serializer.save()
            return Response (guest_user_serializer.data, status=status.HTTP_201_CREATED)
        return Response (guest_user_serializer.errors)


@api_view (["GET","POST"])
def insert_user_relation(request):
    values ={'verified_user_id' : '4', 'non_verified_user_id': '6'}

    if request.method == 'POST':
        user_serializer = UserRelationSerializer (data= values)
        if(user_serializer.is_valid()):
            user_serializer.save()
            return Response (user_serializer.data, status=status.HTTP_201_CREATED)
        return Response (user_serializer.errors)


@api_view (["GET","POST"])
def get_non_verified_user(request,verified_user_id):
  
    if request.method == 'GET':
        try:
            non_verified_user_data = user_relation.objects.get(verified_user_id = verified_user_id)
            user_serializer = UserRelationSerializer (non_verified_user_data, many = False)
            return Response (user_serializer.data)
        except:
            return Response({'Message': 'Some internal problem to retrive data'})

@api_view (["GET","POST"])
def get_verified_user(request,non_verified_user_id):
  
    if request.method == 'GET':
        try:
            verified_user_data = user_relation.objects.get(non_verified_user_id = non_verified_user_id)
            user_serializer = UserRelationSerializer (verified_user_data, many = False)
            return Response (user_serializer.data)
        except:
            return Response({'Message': 'Some internal problem to retrive data'})



#--------------------------- user balance--------------------------

@api_view (["GET","POST"])
def user_balace_value(request):
    '''
    This Api is for retreiving and inserting user balance data. Users has two variation which are verified user and non verified user.
    All sort of users will have user balance function. Initially, the balance field values will be zero or null which will change later upon the 
    user actions. Calling http://127.0.0.1:8000/user/balance/ url will invoke this Api.

    GET Response:
        Following fields are expected while performing the GET request.
        wallet : FloatField (Default value of this field is zero. User can add balance later to their wallet)
        point : FloatField (Deafult value is zero. This field will change upon the user purchase history)
        date : dateField (Deafult time will be shown)
    
    POST Response:
        Following values are expected while performing the POST response.
        wallet : FloatField (By deafult it will be zero. It will be created automatically while calling the specific Api)
        point : FloatFiled (By deafult it will be zero. It will be created automatically while calling the specific Api)
        date : dateField (It will be created automatically while calling the Api)
        user_id : IntegerField (This will act as a foreign key of User table. You must need to provide a valid user_id.)
        ip_id: IntegerField (As there will be two types user varified and non verified. for the non verified user this will act as a foreign key)

    '''
    
    if(request.method == "GET"):
        queryset = user_balance.objects.all()
        balance_serializers = UserBalanceSerializer (queryset,many = True)
        return Response (balance_serializers.data)

    if(request.method == "POST"):
        balance_serializers = UserBalanceSerializer (data= request.data)
        if(balance_serializers.is_valid()):
            balance_serializers.save()
            return Response (balance_serializers.data, status=status.HTTP_201_CREATED)
        return Response (balance_serializers.errors)

@api_view (["GET","POST"])
def specific_user_balace_value(request,user_id):

    if(request.method == "GET"):
        queryset = user_balance.objects.get(user_id=user_id)
        balance_serializers = UserBalanceSerializer (queryset,many = False)
        return Response (balance_serializers.data)


@api_view (["GET","POST"])
@transaction.atomic
def add_wallet_value(request):
    '''
    This Api is for adding balance in individual user wallet. User may add balance to their invividual wallet. This function will 
    be called while user will like to add their balance in wallet. This Api expects, user already performed thier transcation via other 
    api like payment get way. This will just update the wallet column of user balance table. Here, django transcation.atomatic decorator has 
    been used so that Any failure due to internet connection or electricity problem will cause to not updating the value rather it will 
    roll back to previous state. Post request to http://127.0.0.1:8000/user/add_wallet/ url will invoke this Api.

    POST Response:
        This Api expects followings as a POST request:
        value : This can be any integar or float value. This value will be with user wallet.
        varified_user_id or non_verfied_id : User id of either varified or non veried must need to send. This will help to find the user 
        in which account the value will be added.

    '''
    #demo value
    wallet_api_value = {'value': '500', 'user_id':"2"}

    if(request.method == "POST"):

        try:
            user = user_balance.objects.get(user_id= wallet_api_value['user_id'])
            user_wallet = user_balance.objects.filter(user_id= wallet_api_value['user_id']).values('wallet')
            user_wallet_value = user_wallet[0]['wallet'] + float(wallet_api_value['value'])
            user_wallet_values = {'wallet':user_wallet_value}
            
            balance_serializers = UserBalanceSerializer (user,data= user_wallet_values)
            if(balance_serializers.is_valid()):
                balance_serializers.save()
                return Response (balance_serializers.data, status=status.HTTP_201_CREATED)
            return Response (balance_serializers.errors)
        except:
            return Response({'Message': 'Some internal problem to add the value'})


@api_view (["GET","POST"])
@transaction.atomic
def subtract_wallet_value(request):
    '''
    After purchasing products using user wallet, the value of wallet must need to subtract. While requring to perform this action
    this Api will be called. Using user id this Api will find the user wallet balance and will chack whether the balance is greater than the 
    value in whch user wanted to purchase or not. If wallet has higher value then user will be able to buy product using wallet value. If user
    dont have sufficient values, then e messge will be sent to user. Calling http://127.0.0.1:8000/user/subtract_wallet/ will cause to invoke this API.

    POST Response:
        This Api only have POST responses. While performing on the POsT request this Api expects following fields.
        value : This will be integer or float value. This is the value which will be sbtracted from the wallet balance.
        varified_user_id or non_verfied_id : This is the user id which will help to find the desired user from the value will be subtracted.
    '''
    #demo value
    wallet_api_value = {'value': '500', 'user_id':"2"}
   
    if(request.method == "POST"):

        try:
            user = user_balance.objects.get(user_id= wallet_api_value['user_id'])
            user_wallet = user_balance.objects.filter(user_id= wallet_api_value['user_id']).values('wallet')
            
            if((user_wallet[0]['wallet'])>=(float(wallet_api_value['value']))):
                user_wallet_value = user_wallet[0]['wallet'] - float(wallet_api_value['value'])
                user_wallet_values = {'wallet':user_wallet_value}

            else:
                return Response({'Message': 'You do not have sufficient value'})
                 
            balance_serializers = UserBalanceSerializer (user,data= user_wallet_values)
            if(balance_serializers.is_valid()):
                balance_serializers.save()
                return Response (balance_serializers.data, status=status.HTTP_201_CREATED)
            return Response (balance_serializers.errors)
        except:
            return Response({'Message': 'Some internal problem to subtract the value'})

                
@api_view (["GET","POST"])
@transaction.atomic
def point_conversion(request):
    '''
    This Api is for converting the points into currency. Upon puchasing product user will get points. If user have sufficient point and site has set the point converting values
    only then user will be 
    able to convert their points into currency. The information related will currency will come from site settings table. Admin will upload the corresponding
    values in setting tables. After the conversion currency will be added to user wallet which user may use to purchase products later.
    Calling http://127.0.0.1:8000/user/convert_point/ will invoke this API. If any problems occur during the conversion, this Api will send an error message 
    to the user. 

    POST Response :
        This Api only have Post response. While performing post request, this will expect an user id. This field must
        need to provide as it is required to find the user against whom the point will be converted.
    '''
    #demo data
    conversion_api_value = {'user_id':"1",}

    if request.method == "POST":
        try:
    
            user = user_balance.objects.get(user_id= conversion_api_value['user_id'])
            user_point = user_balance.objects.filter(user_id= conversion_api_value['user_id']).values('point')
            user_wallet = user_balance.objects.filter(user_id= conversion_api_value['user_id']).values('wallet')
            site_converted_value = Settings.objects.values('point_converted_value').last()['point_converted_value']
            site_point_value = Settings.objects.values('point_value').last()['point_value']
            if(((user_point[0]['point'])> 0.00) and ((site_converted_value > 1) and (site_point_value>1))):

                point_values = (site_converted_value* (user_point[0]['point']))/ site_point_value
                converted_point_value = user_wallet[0]['wallet'] + point_values
                new_values = {'wallet':converted_point_value, 'point' : '0.00'} 
            else:
                return Response({'Message': 'Some internal problem occurs while converting the point.'})
            
                
            balance_serializers = UserBalanceSerializer (user,data= new_values)
            if(balance_serializers.is_valid()):
                balance_serializers.save()
                return Response (balance_serializers.data, status=status.HTTP_201_CREATED)
            return Response (balance_serializers.errors)
        except:
            return Response({'Message': 'Some internal problem to convert the point value'})



@api_view (["GET","POST"])
def add_point(request):
    '''
    This Api is for adding point to a particular user. User will get points upon their purchasing history. This api will be useful there to add the points to
    the corresponding user. This api just jave POST request. Calling http://127.0.0.1:8000/user/point_add/ will cause to invoke this API.

    POST Response:
        In post response, this Api expects the following fields.
        point : This will be an integer or Float value. This value will be added to the particular user.
        varified or non verified user id : This will be required to find the user to whom the point will be added.
    '''
    #demo values
    point_api_value = {'user_id':"1", 'point' : "1500"}

    if(request.method == "POST"):
        new_point_value={}
        try:
            user = user_balance.objects.get(user_id= point_api_value['user_id'])
            user_point = user_balance.objects.filter(user_id= point_api_value['user_id']).values('point')
            
            user_point_value = user_point[0]['point']+float(point_api_value['point'])
            new_point_value = {'point':user_point_value}
            
               
            balance_serializers = UserBalanceSerializer (user,data= new_point_value)
            if(balance_serializers.is_valid()):
                balance_serializers.save()
                return Response (balance_serializers.data, status=status.HTTP_201_CREATED)
            return Response (balance_serializers.errors)
        except:
            return Response({'Message': 'Some internal problem to subtract the value'})

