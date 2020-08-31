from rest_framework import serializers , exceptions
from Intense.models import User , Profile , Address , user_relation , DeactivateUser,user_balance,Guest_user
from django.contrib import auth 
from rest_framework.exceptions import AuthenticationFailed
from drf_extra_fields.fields import Base64ImageField
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.encoding import smart_str, force_str, smart_bytes, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from rest_framework.validators import UniqueValidator
from rest_framework.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import Permission



class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        max_length=68, min_length=6, write_only=True)

    class Meta:
        model = User
        fields = ['email', 'password']

    def validate(self, attrs):
        email = attrs.get('email', '')
        return attrs

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)


class EmailVerificationSerializer(serializers.ModelSerializer):
    token = serializers.CharField(max_length=555)

    class Meta:
        model = User
        fields = ['token']


class LoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=255, min_length=3)
    password = serializers.CharField(
        max_length=68, min_length=6, write_only=True)
    tokens = serializers.CharField(max_length=68, min_length=6, read_only=True)

    class Meta:
        model = User
        fields = ['email', 'password','tokens']

    def validate(self, attrs):
        email = attrs.get('email', '')
        password = attrs.get('password', '')

        user = auth.authenticate(email=email, password=password)
        if not user:
            raise AuthenticationFailed('Invalid credentials, try again')
        if not user.is_active:
            raise AuthenticationFailed('Account disabled, contact admin')
        if not user.is_verified:
            raise AuthenticationFailed('Email is not verified')

        return {
            'email': user.email,
            'tokens': user.tokens
        }

        return super().validate(attrs)

    def _validate_token(self, tokens):
        user = None

        if tokens:
            user = self.authenticate(tokens=tokens)
        else:
            msg = _('Must include tokens.')
            raise exceptions.ValidationError(msg)

        return user

class ResetPasswordEmailRequestSerializer(serializers.Serializer):
    email = serializers.EmailField(min_length=2)

    class Meta:
        fields = ['email']


class SetNewPasswordSerializer(serializers.Serializer):
    password = serializers.CharField(
        min_length=6, max_length=68, write_only=True)
    token = serializers.CharField(
        min_length=1, write_only=True)
    uidb64 = serializers.CharField(
        min_length=1, write_only=True)

    class Meta:
        fields = ['password', 'token', 'uidb64']

    def validate(self, attrs):
        try:
            password = attrs.get('password')
            token = attrs.get('token')
            uidb64 = attrs.get('uidb64')

            id = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(id=id)
            if not PasswordResetTokenGenerator().check_token(user, token):
                raise AuthenticationFailed('The reset link is invalid', 401)

            user.set_password(password)
            user.save()

            return (user)
        except Exception as e:
            raise AuthenticationFailed('The reset link is invalid', 401)
        return super().validate(attrs)




# class ProfileSerializer(serializers.ModelSerializer):
#     user = serializers.SlugRelatedField(slug_field='email',read_only=True)
#     gender = serializers.SerializerMethodField()
#     profile_picture = Base64ImageField()

#     def get_gender(self, obj):
#         return obj.get_gender_display()

#     class Meta:
#         model = Profile
#         fields = "__all__"
#     '''
#     TODO update profile and if Email is not verified user can't update in his profile.
#     '''

class ProfileSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Profile
        fields = "__all__"
 
class UserSerializer(serializers.ModelSerializer):
    profile_picture = serializers.ImageField(source='profile.profile_picture')
    gender = serializers.CharField(source='profile.gender')
    about = serializers.CharField(source='profile.about')
    phone_number = serializers.CharField(source='profile.phone_number')

    class Meta:
        model = User()
        fields = "__all__"



class CustomRegisterSerializer(RegisterSerializer):
    first_name = serializers.CharField(required=True, write_only=True)
    last_name = serializers.CharField(required=True, write_only=True)
    phone_number =  serializers.CharField(required=True, write_only=True , 
                                    validators = [UniqueValidator(
                                        queryset = Profile.objects.all(),
                                        message = _("A user is already registered with this phone number."))])

    def get_cleaned_data_profile(self):
        return {
            'first_name': self.validated_data.get('first_name', ''),
            'last_name': self.validated_data.get('last_name', ''),
            'phone_number': self.validated_data.get('phone_number', '')
        }

    def create_profile(self, user, validated_data):
        user.first_name = self.validated_data.get('first_name')
        user.last_name = self.validated_data.get('last_name')
        user.save()

        user.profile.phone_number = self.validated_data.get('phone_number')
        user.profile.save()

    def custom_signup(self, request, user):
        self.create_profile(user, self.get_cleaned_data_profile()) 



class UserMiniSerializer(serializers.ModelSerializer):
    profile_picture = serializers.ImageField(source='profile.profile_picture')
    gender = serializers.CharField(source='profile.gender')
    phone_number = serializers.CharField(source='profile.phone_number')

    class Meta:
        model = User()
        fields = "__all__"

class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = "__all__"

class CreateAddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        exclude = ['primary', 'user']



class UserRelationSerializer(serializers.ModelSerializer):
     
   class Meta:
        model = user_relation
        fields = ('id','verified_user_id','non_verified_user_id')


class DeactivateUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = DeactivateUser
        exclude = ["deactive", "user"]



class PermissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Permission
        fields = ['email', 'codename', 'content_type']


class UserPermissionretriveSerializer(serializers.ModelSerializer):
    user_permissions = PermissionSerializer(many=True, read_only=True)
    class Meta:
        model = User
        fields = ('user_permissions',)

class UserPermissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('user_permissions',)

class UserBalanceSerializer(serializers.ModelSerializer):
   
    class Meta:
        model = user_balance
        #fields = "__all__"
        fields=("id","wallet", "point", "dates", "user_id")


class GuestUserSerializer(serializers.ModelSerializer):
   
    class Meta:
        model = Guest_user
        fields = "__all__"


