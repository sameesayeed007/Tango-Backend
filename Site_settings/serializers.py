from rest_framework import serializers
from Intense.models import CompanyInfo,Banner,RolesPermissions,Banner_Image,Currency,Settings,APIs,Theme,FAQ
from django.conf import settings
from django.contrib.sites.shortcuts import get_current_site

#site_path = str(settings.BASE_DIR)
current_site = Site.objects.get_current()
class CompanyInfoSerializer(serializers.ModelSerializer):
    '''
    This serializer is for Company Info model and funtionalities.
    It will return all the fields in the compnay info model class in case of GET and POsT request.
    fields:
            name: CharField, max_length=500,
            logo: ArrayField,
            address: TextField, max_length=1500,
            icon: ArrayField,
            Facebook: CharField,max_length=264,
            twitter : CharField,max_length=264,
            linkedin: CharField,max_length=264,
            youtube: CharField,max_length=264,
            email: CharField,max_length=264,
            phone: CharField,max_length=264,
            help_center: harField,max_length=264,
            About: CharField,max_length=5000,
            policy: ArrayField , max_length = 100000,
            terms_condition: ArrayFiled, max_length=100000,
            role_id : IntegerFiled, max_length= 264,
            slogan: CharField,max_length=264,
            cookies: CharField,max_length=100000
    '''
    logo_url = serializers.SerializerMethodField(method_name='get_logo')
    icon_url = serializers.SerializerMethodField(method_name='get_icon')
    class Meta:
        model = CompanyInfo
        #fields = "__all__"
        fields=("name", "logo","address","icon","Facebook","twitter","linkedin","youtube","email","phone","help_center","About","policy","terms_condition","slogan","cookies","logo_url","icon_url")

    def get_logo(self,instance):

        try:
            logo_image = CompanyInfo.objects.all().first()
        except:
            logo_image = None

        if logo_image is not None:
            logo = logo_image.logo
            return "{0}{1}".format(current_site,logo.url)

        else:
            return " "


    def get_icon(self,instance):

        try:
            logo_image = CompanyInfo.objects.all().first()
        except:
            logo_image = None

        if logo_image is not None:
            logo = logo_image.icon
            return "{0}{1}".format(current_site,logo.url)

        else:
            return " "


class BannerSerializer(serializers.ModelSerializer):
    '''
    This serializer is for Banner model and funtionalities.
    It will return all the fields in the Banner model class in case of GET and POsT request.
    fields:

        count: IntegerField
        set_time: IntegerField
        role_id: IntegerField
    
    '''
    class Meta:
        model = Banner
        fields = "__all__"
        #fields=("count", "link")

class BannerImageSerializer(serializers.ModelSerializer):
    '''
    This serializer is for Banner image upload model and funtionalities.
    It will return all the fields in the Banner image  model class in case of GET and POsT request.
    fields:

        image: ImageField,
        link: CharField,max_length=500,
        content : CharField,max_length=264,
    
    '''
 
    class Meta:
        model = Banner_Image
        fields = "__all__"
       

class RolesPermissionsSerializer(serializers.ModelSerializer):
    '''
    This serializer is for Roles and Permission model and funtionalities.
    It will return all the fields in the Banner model class in case of GET and POsT request.
    fields:

        roleType: CharField,max_length=500,
        roleDetails : CharField,max_length=264
        
    '''
    class Meta:
        model = RolesPermissions
        fields = "__all__"
        #fields=("roleType", "roleDetails")

class CurrencySerializer (serializers.ModelSerializer):
    '''
    This serializer is to get access all the values from currency table.
    '''

    class Meta:
        model = Currency
        fields = ("id","currency_type", "value", "dates")

class SettingsSerializer (serializers.ModelSerializer):

    class Meta:
        model = Settings
        fields = ("id","tax", "vat","point_value","point_converted_value")
        #fileds = "__all__"

class ThemeSerializer (serializers.ModelSerializer):

    class Meta:
        model = Theme
        fields = "__all__"

class APIsSerializer (serializers.ModelSerializer):

    class Meta:
        model = APIs
        fields = "__all__"

class FaqSerializer (serializers.ModelSerializer):
    class Meta:
        model = FAQ
        fields = "__all__"
