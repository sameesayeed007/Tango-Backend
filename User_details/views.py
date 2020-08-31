from django.shortcuts import render , redirect
from rest_framework import generics, status, views
from .serializers import RegisterSerializer, SetNewPasswordSerializer, DeactivateUserSerializer,UserBalanceSerializer, UserPermissionSerializer,UserPermissionretriveSerializer,PermissionSerializer, ResetPasswordEmailRequestSerializer, EmailVerificationSerializer,UserRelationSerializer, LoginSerializer , UserSerializer   , AddressSerializer , CreateAddressSerializer , ProfileSerializer,GuestUserSerializer
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from Intense.models import User , user_relation,Settings,user_balance

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
from Intense.models import Profile, Address, User ,DeactivateUser , user_relation,Guest_user

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from .decorators import unauthenticated_user, allowed_users, admin_only
from django.contrib import messages
from django.db import transaction
from Intense.Integral_apis import create_user_balance,create_user_profile


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

class LoginAPIView(generics.GenericAPIView):
    '''
    This is user Login Api.
    '''
    serializer_class = LoginSerializer

    def post(self, request):
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
        try:

            user_profile = Profile.objects.get(user_id = user_id)
            user_profile_serializer = ProfileSerializer (user_profile, many = False)
            return Response (user_profile_serializer.data)
        except:
            return Response({'Message': 'Some internal problem to retrive data'})

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
        


class UserDetailView(RetrieveAPIView):
    # permission_classes = [auth.authenticate]
    serializer_class = UserSerializer
    queryset = User.objects.all()
    lookup_field = 'username'

class ListAddressAPIView(ListAPIView):
    # permission_classes = [auth.authenticate]
    serializer_class = AddressSerializer

    def get_queryset(self):
        user = self.request.user
        queryset = Address.objects.filter(user=user)
        return queryset

class AddressDetailView(RetrieveAPIView):
    # permission_classes = [auth.authenticate]
    serializer_class = AddressSerializer
    queryset = Address.objects.all()

    def retrieve(self, request, *args, **kwargs):
        user = request.user
        address = self.get_object()
        if address.user != user:
            raise NotAcceptable("this addrss don't belong to you")
        serializer = self.get_serializer(address)
        return Response(serializer.data, status=status.HTTP_200_OK)

class createAddressAPIView(CreateAPIView):
    # permission_classes = [auth.authenticate]
    serializer_class = CreateAddressSerializer
    queryset = ''

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=request.user, primary=True)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


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




class DeactivateUserView(CreateAPIView):
    # permission_classes = [auth.authenticate]
    serializer_class = DeactivateUserSerializer

    def create(self, request, *args, **kwargs):
        user = request.user
        # TODO validation and try exception
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=user)
        return Response("your account will deactivate after 30 days.")


class CanselDeactivateUserView(APIView):
    # permission_classes = [auth.authenticate]

    def post(self, request, *args, **kwargs):
        user = request.user
        # TODO validation and try exception
        deactivate = DeactivateUser.objects.get(user=user)
        deactivate.deactive = False
        deactivate.save()
        user.is_active = True
        user.save()
        return Response("your account will activated.")

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

