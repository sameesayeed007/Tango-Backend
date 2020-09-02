from django.shortcuts import render
from rest_framework.decorators import api_view
from Intense.models import CompanyInfo,Banner,RolesPermissions,Banner_Image,Currency,Settings,Theme,APIs,FAQ,ContactUs
from .serializers import CompanyInfoSerializer,BannerSerializer,RolesPermissionsSerializer,BannerImageSerializer,CurrencySerializer,SettingsSerializer
from .serializers import ThemeSerializer,APIsSerializer,FaqSerializer,ContactUsSerializer
from rest_framework.response import Response
from rest_framework import status
from Intense.utils import get_image,get_roles_id
import datetime
# Create your views here.

@api_view (["GET","POST"])
def CompanyInfos(request):

    '''
    This is Compnay Info API.
    This api will be invoked after calling url : localhost:8000/site/info
    This API expected JSON format data. It uses get_image function to resize the logo and icon images.
    This API is developed using rest framework and serializers.
    POST request expected arguments:
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

    GET request expected response:
        name: CharField,
        logo: ArrayField,
        address: TextField,
        icon: ArrayField,
        Facebook: CharField,
        twitter : CharField,
        linkedin: CharField,
        youtube: CharField,
        email: CharField,
        phone: CharField,
        help_center: harField,
        About: CharField,
        policy: ArrayField,
        terms_condition: ArrayFiled,
        role_id : IntegerFiled,
        slogan: CharField,
        cookies: CharField

    '''
    if(request.method == "GET"):
        try:
            queryset = CompanyInfo.objects.all()
            

            serializers = CompanyInfoSerializer (queryset,many = True)
           
            return Response (serializers.data)
        except:
            return Response({'message': 'There is no information to display'})

    elif(request.method == "POST"):

        # This data will come from frontend API
        Info_Api_data = {'name': "intense", 'address': "Glafasha Plaza", 'Facebook': "facebook.com", 'twitter': "twitter.com",
        'linkedin': "linkedin.com", 'youtube': "youtube.com", 'email': "abc@gmail.com", 'phone': "017494",'help_center': "+880", 'About': "we are", 
        'policy': ["some", "policies"], 'terms_condition': ["terms", "conditions"], 'role_id': "1", 'slogan': "Some slogan", 'cookies': "cookis"}
        
        serializers = CompanyInfoSerializer (data= Info_Api_data)
        if(serializers.is_valid()):
            serializers.save()
            return Response (serializers.data, status=status.HTTP_201_CREATED)
        return Response (serializers.errors)
            
       
@api_view(['POST','GET'])
def update_CompanyInfos(request):
    '''
        This Api is for update a particular company information. It is assumes that, for a particular company there will be exactly one information.
        In case of multiple information, always it will retrive last added information and will be availabe for update. 
        Calling  http://127.0.0.1:8000/site/update_info will invoke this Api.
        
    '''
    try:
        queryset = CompanyInfo.objects.all().last()
    
    except :
        return Response({'message': 'This value does not exist'})

    if request.method == 'GET':
        serializers = CompanyInfoSerializer (queryset,many = False)
        return Response (serializers.data)
 
    elif request.method == "POST" :
        try:
            serializers = CompanyInfoSerializer (queryset, data= request.data)
            if(serializers.is_valid()):
                serializers.save()
                return Response (serializers.data, status=status.HTTP_201_CREATED)
            return Response (serializers.errors)
        except:
            return Response({'message': 'Information could not be updated'})

        
@api_view(['POST','GET'])
def delete_CompanyInfos(request,info_id):

    # This API is for deleting company informations. 
    # This API will be invoked after calling : http://127.0.0.1:8000/site/delete_info/1/
    # dmin will have the permission to delete and add company informations.
    # If requested information is not present in the database then this API will through a message saying there is no information.
    # If the information is present this will delete the requested information and after deleting it will through successfull message.

	try:
		companyInfo= CompanyInfo.objects.get(pk = info_id)
		if request.method == 'POST':
			companyInfo.delete()
			return Response({'message': 'Company Informations is deleted successfully!'}, status=status.HTTP_204_NO_CONTENT)

	except:
		return Response({'message': 'There is no infomation'})


@api_view (["GET","POST"])
def get_specific_Banners(request,banner_id):

    '''
    This is for getting specific Banner. Site does have multiple banner and in each banner there will be multiple images. While performing the 
    Get request it will have following response. While calling this API, desired banner id must need to be sent. Calling http://127.0.0.1:8000/site/banner/14
    will cause to invoke this Api.

    Get Response:
        In get response it will send banner related information as an object and images as an array filed. Follwoing is the get response for tjis Api.

    [
        {
            "id": 14,
            "count": 2,
            "set_time": 3
        },
        [
            {
                "id": 22,
                "Banner_id": 14,
                "image": null,
                "link": "abc.link",
                "content": "content"
            },
            {
                "id": 23,
                "Banner_id": 14,
                "image": null,
                "link": "efg.link",
                "content": "nothing"
            }
        ]
    ]

    '''



    if(request.method == "GET"):
        try:
            queryset = Banner.objects.get(pk= banner_id)
        except:
            queryset = None
        if queryset is not None:

            serializers = BannerSerializer (queryset,many = False)
            banner_image = Banner_Image.objects.filter(Banner_id = banner_id)
            image_serializers = BannerImageSerializer (banner_image,many = True)
            #banner_data = [serializers.data,image_serializers.data]
            return Response({
                'success': True,
                'message': 'The values are inserted below',
                'banner_data': serializers.data ,
                'images' : image_serializers.data
                })

        else:
            return Response({
                'success': False,
                'message': 'There are no values to show',
                'data': ''
                })

            
        
            

@api_view (["GET","POST"])
def Banner_Insertion(request):
    '''
    This Api is for inserting data into the banner. Data will be inserted here through the Post request. Calling http://127.0.0.1:8000/site/banner_insert/ 
    will cause to invoke this api. While performing the Post response it expects data according the following structures.

    post Response:
    {   'count': '2', 
        'set_time': '3', 
        'images': 
            [
                {
                    'link': "abc.link", 
                    'content': "content"
                },
                { 
                    'link': "efg.link", 
                    'content': "nothing"
                }
            ]
    }

    '''

    if request.method == "POST":
        try:
            api_banner_data = {'count': '2', 'set_time': '3', 'images': [{'link': "abc.link", 'content': "content"},
            { 'link': "efg.link", 'content': "nothing"}]}
            banner_data = {'count': api_banner_data['count'], 'set_time': api_banner_data['set_time']}
            serializers = BannerSerializer (data= banner_data)
            if(serializers.is_valid()):
                serializers.save()
            banner_id = Banner.objects.latest('id')
            for val in api_banner_data['images']:
                val.update( {'Banner_id' : banner_id.pk} )
                banner_serializers = BannerImageSerializer (data= val)
                if(banner_serializers.is_valid()):
                    banner_serializers.save()  
            return Response ({'message': 'Value successfully added'})
        except:
             return Response ({'message': 'Some internal problem occurs'})


@api_view (["GET","POST"])
def Banner_value_update(request,banner_id):
    '''
    This field is to update banner related information like updating time. Calling http://127.0.0.1:8000/site/banner_value_update/16 will cause to invoke 
    this Api. While calling this Api, desired banner id needs to be sent.

    Get Response:
        {
            "id": 16,
            "count": 500,
            "set_time": 3
        } 
    Post Response:
        After updating set time the response will be:
        {
            "id": 16,
            "count": 500,
            "set_time": 30
        }
    '''
    try:
        queryset = Banner.objects.get(pk= banner_id)
    except:
        return Response ({'message': 'There is no value'})

    if(request.method == "GET"):
        serializers = BannerSerializer (queryset,many = False)
        return Response (serializers.data)

    if request.method == "POST":
        serializers = BannerSerializer (queryset,data= request.data)
        if(serializers.is_valid()):
            serializers.save()
            return Response (serializers.data, status=status.HTTP_201_CREATED)
        return Response (serializers.errors)


@api_view (["GET","POST"])
def Banner_image_add(request,banner_id):
    '''
    This Api is for adding banner image in an existing banner. Calling http://127.0.0.1:8000/site/banner_img_update/16 will cause to invoke this Api.
    While calling this Api, banner_id must need to be sent in parameter.
    '''
    try:
        banner_image = Banner_Image.objects.filter(Banner_id = banner_id)
    except:
        return Response ({'message': 'There is no value'})

    if(request.method == "GET"):
        serializers = BannerImageSerializer (banner_image,many = True)
        return Response (serializers.data)

    if request.method == "POST":
        value = request.data.copy()
        value.update( {'Banner_id' : banner_id} )
        serializers = BannerImageSerializer (data= value)
        if(serializers.is_valid()):
            serializers.save()
            return Response (serializers.data, status=status.HTTP_201_CREATED)
        return Response (serializers.errors)

@api_view (["GET","POST"])
def Banner_image_delete(request,banner_id,img_id):
    '''
    This Api is for deleting specific banner image within the banner. While performing this operation, banner id, in which that specific image belongs 
    and the specific image id must need to be provided. Calling http://127.0.0.1:8000/site/banner_img_delete/16/30/ will cause to invoke this Api.
    '''
   
    banner_image = Banner_Image.objects.filter(Banner_id = banner_id,pk=img_id)
    print(banner_image)
    if request.method == "POST":
        if banner_image.exists():
            banner_image.delete()
            return Response({'message': 'Banner image is deleted successfully!'}, status=status.HTTP_204_NO_CONTENT)
        else:

            return Response ({'message': 'There is no value'})

@api_view(['POST','GET'])
def delete_Banner(request,banner_id):
    '''
    This API for deleting the banner. As there will be only one banner for each site, therefore calling this API will cause to delete 
    all the banner related information. If the delete action is performed, this will send a message to user.
    This API will be invoked after calling : http://127.0.0.1:8000/site/delete_banner/
    '''
    try:
        Banners = Banner.objects.get(pk= banner_id)
        banner_image = Banner_Image.objects.filter(Banner_id = banner_id)
        if request.method == 'POST':
            Banners.delete()
            banner_image.delete()
            return Response({'message': 'Banner is deleted successfully!'}, status=status.HTTP_204_NO_CONTENT)
    except Banner.DoesNotExist:
        return Response({'message': 'There is no infomation to delete'})


@api_view (["GET","POST"])
def All_Roles (request):

    '''
    This is Roles and Permissions API.
    This api will be invoked after calling url : localhost:8000/site/roles
    All the field of this api is expected from front end.
    This API is developed using rest framework and serializers.

    POST request expected arguments:
        roleType: CharField, max_length=264,
        roleDetails: CharField, max_length=264
    
    GET request expected arguments:
        roleType: CharField,
        roleDetails: CharField
    '''
    if(request.method == "GET"):
        queryset = RolesPermissions.objects.all()
        serializers = RolesPermissionsSerializer (queryset,many = True)
        return Response (serializers.data)

    elif(request.method == "POST"):
        serializers = RolesPermissionsSerializer (data= request.data)
        if(serializers.is_valid()):
            serializers.save()
            return Response (serializers.data, status=status.HTTP_201_CREATED)
        return Response (serializers.errors)

@api_view (["GET","POST"])
def Specific_Roles (request,roles_id):

    '''
    This API is for retriving and updating a particular roles information.
    This api will be invoked after calling url : localhost:8000/site/specific_roles/id
    This API will first check whether particular roles is exists in the database or not. If roles does not exist, it will 
    through an error. If role is found, it will retrive and update the necessary informations.
    This API is developed using rest framework and serializers.

    POST request expected arguments:
        roleType: CharField, max_length=264,
        roleDetails: CharField, max_length=264
    
    GET request expected arguments:
        roleType: CharField,
        roleDetails: CharField
    '''
    try: 
        Roles = RolesPermissions.objects.get(pk = roles_id)
    except:
        return Response({'message': 'This Role does not exist'}, status=status.HTTP_404_NOT_FOUND)

    if(request.method == "GET"):
        Roles_serializer = RolesPermissionsSerializer(Roles, many=False)
        return Response (Roles_serializer.data)

    elif(request.method == "POST"):
        Roles = RolesPermissions.objects.get(pk = roles_id)
        Roles_serializers = RolesPermissionsSerializer(Roles,data= request.data)
        if(Roles_serializers.is_valid()):
            Roles_serializers.save()
            return Response (Roles_serializers.data, status=status.HTTP_201_CREATED)
        return Response (Roles_serializers.errors)


@api_view(['POST','GET'])
def delete_Roles(request,role_id):
    
    # This API for deleting the Roles. This API will delted the Roles information based on the provided id.
    # If the delete action is performed, this will send a message to user.
    # This API will be invoked after calling : http://127.0.0.1:8000/site/delete_role/1/
    
	
    Roles= RolesPermissions.objects.filter(pk = role_id)
    if request.method == 'POST':
        if Roles.exists():
            Roles.delete()
            return Response({'message': 'Roles and Permissions has been deleted successfully!'}, status=status.HTTP_204_NO_CONTENT)
        else:
            return Response({'message': 'There is no Roles and Permissions infomation to delete'})


		
# ------------------------------------------------------------------------------------------------------------------------------------
@api_view (["GET","POST"])
def Currency_value (request):

    '''
    This API is for adding and retriving values to currency table. The default currency of a site will be taka and Currency database will
    store currecncy value compare will per unit taka. For example, 1 dollar = 85 taka. It will store currency type as dollar and value 85. 
    For default value will be 1. After being called, this API will provide all the values from the currency table. 
    This API can be called using : http://127.0.0.1:8000/site/currency/
    GET Response:
        After the get response this will return all the information of the currency table database including the follwoing fields:
        currency_type : deafult taka,
        value : FloatField,
        dates : date and Time field

    POST Response:
        Post response will store the value into the currency table. The fileds are following:
        currency_type : CharField (default taka)
        value : float (for taka it will be deafult 01.00)
        dates: Date and Time field,
        role_id : IntegerField(This will act as a foriegn key)
    '''
    currency_api_data = {'currency_type': "Dollar", 'value': "85.00", 'dates': "12-08-2020",'role_id': "Admin"}
    if(request.method == "GET"):
        currency_data = Currency.objects.all()
        currency_serializers = CurrencySerializer (currency_data, many = True)
        return Response (currency_serializers.data)

    elif(request.method == "POST"):
        currency_data={}
        if(get_roles_id(currency_api_data['role_id']) is not None):
            currency_data = {'currency_type': currency_api_data['currency_type'], 'value': currency_api_data['value'],
            'dates': currency_api_data['dates'],'role_id': get_roles_id(currency_api_data['role_id'])}

            currency_serializers = CurrencySerializer (data= currency_data)
            if(currency_serializers.is_valid()):
                currency_serializers.save()
                return Response (currency_serializers.data, status=status.HTTP_201_CREATED)
            return Response (currency_serializers.errors)
        else:
            return Response({'message': 'Please make sure you have Roles value'})

       
@api_view (["GET","POST"])
def latest_Currency_value (request):

    '''
    This API is for getting the last currency data based on date. This is required while calculating the product price. Currency table 
    will have multiple currency values but for the calculation always latest data will be used.
    This API will be invoked after calling : http://127.0.0.1:8000/site/last_currency/
    GET Response:
        After the get response this will return the last entry of the currency table database including the follwoing fields:
        currency_type : deafult taka,
        value : FloatField,
        dates : date and Time field
    '''
    if(request.method == "GET"):
        last_currency_data = Currency.objects.latest("dates")
        last_currency_serializers = CurrencySerializer (last_currency_data)
        return Response (last_currency_serializers.data)

@api_view (["GET","POST"])
def Specific_Currency_get_delete (request,currency_id):

    '''
    This is for retriving and deleting a particular currency data. Admin will have the access to retrive and delete the data.
    This API will be invoked after calling: http://127.0.0.1:8000/site/specific_currency/6 
    GET Response:
        If the requested value exists it will send all the data of that specific id. If requested data is not present, it will through a message 
        as a response.
    POST Response:
        After successfully deleting a value, it will send a successful message as a response.
    '''
    try: 
        currency_value = Currency.objects.get(pk = currency_id)
    except :
        return Response({'message': 'This value does not exist'})

    if request.method == "GET" :
    
        currency_serializer_value= CurrencySerializer(currency_value, many=False)
        return Response (currency_serializer_value.data)

    elif request.method == 'POST':
        currency_value.delete()
        return Response({'message': 'Currency value has been deleted successfully!'})


# -----------------------------------------------------------------------------------------------

@api_view (["GET", "POST"])
def all_theme_infos(request):
    '''
    This API is for inserting and retreiving all the theme infos data. Site admin or anyone having special permission will have access to 
    add and change the theme. If no theme is added, the deafult theme will be used as the site theme. 
    This API will be revoked after calling : http://127.0.0.1:8000/site/theme/ . Simply calling this API will cause to integrate with front end.
    GET Response:
        id : IntegerField (This is the primary key)
        name : Charfield (This is the name of the theme)
        details : CharFiled (Any description related the theme or pros and cons will be in this column.)

    POST Response:
        This API expected following fields while integrating with the others throug post request.
        name : CharField (CharFiled containg name must need to provide)
        details : CharFiled (It expects details to be provided while integrating through Post request)

    '''
    if request.method == 'GET':
        Theme_value= Theme.objects.all()
        theme_serializer_value = ThemeSerializer (Theme_value, many = True)
        return Response (theme_serializer_value.data)

    if request.method == 'POST':
        theme_serializers_value = ThemeSerializer (data= request.data)
        if(theme_serializers_value.is_valid()):
            theme_serializers_value.save()
            return Response (theme_serializers_value.data, status=status.HTTP_201_CREATED)
        return Response (theme_serializers_value.errors)

@api_view (["GET","POST"])
def Specific_theme (request,theme_id):
    '''
    This API is for retriving and updating a particular theme data. This Api will find the requested theme through the id number. If it gets the desired 
    information it will send it to update via get request and through post request it will update the requested information in a particular data. 
    Simply calling http://127.0.0.1:8000/site/specific_theme/1 will cause to integrate this Api.
    GET Response:
        id : IntegerField (This is the primary key of the requested field)
        name : Charfield (This is the name of the theme of the requested field)
        details : CharFiled (Any description related the theme or pros and cons of the requested field will be in this column.)

    POST Response:
        This API expected following fields while making post request after the value updatation.
        name : CharField (CharFiled containg name must need to provide)
        details : CharFiled (It expects details to be provided while integrating through Post request)

    '''

    try: 
        theme = Theme.objects.get(pk = theme_id)
    except :
        return Response({'message': 'This Theme does not exist'})

    if(request.method == "GET"):
        themes_serializer = ThemeSerializer(theme, many=False)
        return Response (themes_serializer.data)

    elif(request.method == "POST"):
        themes_serializer = ThemeSerializer(theme,data= request.data)
        if(themes_serializer.is_valid()):
            themes_serializer.save()
            return Response (themes_serializer.data, status=status.HTTP_201_CREATED)
        return Response (themes_serializer.errors)
        
@api_view(['POST','GET'])
def delete_theme(request,theme_id):
    
    # This API is for deleting a particular theme entity. This Api will find the requested theme through the id number. If it gets the desired 
    # information it will delete the information and will send a successful message as response. In case of any failure, it will send an error message 
    # as a response. Simply calling http://127.0.0.1:8000/site/theme_delete/1 will cause to integrate this Api.
    
	try:
		themes_value= Theme.objects.get(pk = theme_id)
		if request.method == 'POST':
			themes_value.delete()
			return Response({'message': 'Theme is deleted successfully!'}, status=status.HTTP_204_NO_CONTENT)

	except :
		return Response({'message': 'There is no infomation to delete'})


@api_view (["GET", "POST"])
def all_APIs_infos(request):
    '''
    This Api is for retreving and inserting the third party APIs which are integrated with the site. All the third party integrated Apis will
    be stored in APIs table having name and details information. Admin or individual with special permission will have the access add new integrated API 
    in this table through this API or retreving all the third party api related information. Simple calling http://127.0.0.1:8000/site/Api/ will cause 
    to integrate this Api.

    GET Response :
        While getting the GET request it will send the following information:
        id : IntegerField ( This is the primary key)
        name : CharField ( This will be the name of the API)
        details : CharField ( This will be the details information of the API)

    POST Response:
        While getting the POST request this api expected following values:
        name : CharField (This will be the name of the API. Basically a string)
        details : Charfield ( This will be the details information of that particular API. This will also be a string)
    '''
    if request.method == 'GET':
        Api_value= APIs.objects.all()
        Api_serializer_value = APIsSerializer (Api_value, many = True)
        return Response (Api_serializer_value.data)

    if request.method == 'POST':
        Api_serializer_value = APIsSerializer (data= request.data)
        if(Api_serializer_value.is_valid()):
            Api_serializer_value.save()
            return Response (Api_serializer_value.data, status=status.HTTP_201_CREATED)
        return Response (Api_serializer_value.errors)

@api_view (["GET","POST"])
def Specific_Api (request,Api_id):
    '''
    This API is for retreiving and updating a particular information of an Api. This Api will find the requested Api through the id number. 
    If it gets the desired information it will send it to update via get request and through post request it will update the requested information 
    in a particular data. Simply calling http://127.0.0.1:8000/site/specific_Api/1 will cause to integrate this Api.

    GET Response:
        id : IntegerField (This is the primary key of the requested field)
        name : Charfield (This is the name of the theme of the requested field)
        details : CharFiled (Any description related the theme or pros and cons of the requested field will be in this column.)

    POST Response:
        This API expected following fields while making post request after the value updatation.
        name : CharField (CharFiled containg name must need to provide)
        details : CharFiled (It expects details to be provided while integrating through Post request)

    '''

    try: 
        Api = APIs.objects.get(pk = Api_id)
    except :
        return Response({'message': 'This Theme does not exist'})

    if(request.method == "GET"):
        Api_serializer_value = APIsSerializer(Api, many=False)
        return Response (Api_serializer_value.data)

    elif(request.method == "POST"):
        Api_serializer_value = APIsSerializer(Api,data= request.data)
        if(Api_serializer_value.is_valid()):
            Api_serializer_value.save()
            return Response (Api_serializer_value.data, status=status.HTTP_201_CREATED)
        return Response (Api_serializer_value.errors)
        
@api_view(['POST','GET'])
def delete_Api(request,Api_id):
    
    # This API is for deleting a particular Api entity. This Api will find the requested Api through the id number. If it gets the desired 
    # information it will delete the information and will send a successful message as response. In case of any failure, it will send an error message 
    # as a response. Simply calling http://127.0.0.1:8000/site/Api_delete/1 will cause to integrate this Api.
    
	try:
		Api_value= APIs.objects.get(pk = Api_id)
		if request.method == 'POST':
			Api_value.delete()
			return Response({'message': 'Api is deleted successfully!'}, status=status.HTTP_204_NO_CONTENT)

	except :
		return Response({'message': 'There is no infomation to delete'})

@api_view (["GET", "POST"])
def site_all_settings(request):
    '''
    This api is for site settings. All the site related information will be inserted and retreving through this Api. Site settings will be created once 
    and there will be delete option. Destroying the site will cause to delete this table. The site related information can be taken while developing the
    site or later via update. Simply calling http://127.0.0.1:8000/site/settings/ will cause to integrate this Api.

    GET response:
        While getting the get response it is expected to return the following fields
        id : IntegerField (This is the primary key)
        tax : FloatFiled (This will be a float value in a percentage. Example : tax = 5 means 5 %. This tax will be applied to all the price of the products)
        vat : FloatFiled (Like tax it will also be in percentage. This will be used to calculate price where required)
        point_value : FloatField (This point is the reward point. The idea here is to add the points based on the purchachisng. And point values need to be
                    converted into taka which will be saved into user wallet. This field will contain the corresponding point values to make a particular 
                    amount of money. For example : 1000 points = 10 taka. Here 1000 points will be stored)

        point_converted_value : FloatFiled ( This will store the corresnponding money of the points. from the example 1000 points = 10 taka, it will store 
                                10 taka. This value will be used while updating user wallet.)
    
    POST response:
        While getting the post response this api expect following values:
        tax : FloatField (a value wich will be converted in percentage. example : inserting 5 here means 5%)
        vat : FloatFiled (Same as tax)
        point_value : FloatFiled (Number of point wchi will be converted later to corresponding money and will save in user wallet)
        point_converted_value : FloatField (The amount which will be the value after acheiving a certain amount of point)
    
    Additionally it expects follwoing two filed. These two will be required to get the corresponding id which will act as the foreign key. The name of
    this two field must be same.
        role : expects a filed name 'role' having the user roles like Admin/ Suppot. using this a query will be perfomred to RolesAndPermission table 
               to get the corresponding id. Then the corresponding id will be stored as a foreign key.
        theme : expects a field name 'theme' having the theme name like Dark/Night. like role this will be used to perform query theme table to 
                get the corresponding id which will be added to the settings table as foreign key.
    
    Note: Before inserting the values please make sure, keys which will act as foreign key having proper data in their corresponding table.
        
    '''
    if request.method == 'GET':
        settings_value= Settings.objects.all()
        settings_serializer_value = SettingsSerializer (settings_value, many = True)
        return Response (settings_serializer_value.data)

    if request.method == 'POST':
        # role = request.data['role']
        # theme = request.data['theme']
        try:
            # role_id = RolesPermissions.objects.filter(roleType= role).values('id')
            # theme_id = Theme.objects.filter(name = theme).values('id')
           
            # settings_values = {'tax': request.data['tax'], 'vat': request.data['vat'], 'role_id': '2', 'point_value': request.data['point_value'],
            # 'point_converted_value':request.data['point_converted_value'],'theme_id': '3'}
            settings_serializers_value = SettingsSerializer (data= request.data)
            if(settings_serializers_value.is_valid()):
                settings_serializers_value.save()
                return Response (settings_serializers_value.data, status=status.HTTP_201_CREATED)
            return Response (settings_serializers_value.errors)
        except:
            return Response({'message': 'It occurs some problem to insert values'})

@api_view (["GET","POST"])
def settings_update (request,setting_id):
    '''
    This api is for updating the site information. Simply calling http://127.0.0.1:8000/site/update_setting/1 will cause to integrate this Api.

    GET response:
        While getting the get response it is expected to return the following fields of the requested data
        id : IntegerField (This is the primary key)
        tax : FloatFiled (This will be a float value in a percentage. Example : tax = 5 means 5 %. This tax will be applied to all the price of the products)
        vat : FloatFiled (Like tax it will also be in percentage. This will be used to calculate price where required)
        point_value : FloatField (This point is the reward point. The idea here is to add the points based on the purchachisng. And point values need to be
                    converted into taka which will be saved into user wallet. This field will contain the corresponding point values to make a particular 
                    amount of money. For example : 1000 points = 10 taka. Here 1000 points will be stored)

        point_converted_value : FloatFiled ( This will store the corresnponding money of the points. from the example 1000 points = 10 taka, it will store 
                                10 taka. This value will be used while updating user wallet.)
    
    POST response:
        While getting the post response this api expect following values:
        tax : FloatField (a value wich will be converted in percentage. example : inserting 5 here means 5%)
        vat : FloatFiled (Same as tax)
        point_value : FloatFiled (Number of point wchi will be converted later to corresponding money and will save in user wallet)
        point_converted_value : FloatField (The amount which will be the value after acheiving a certain amount of point)
    
    Additionally it expects follwoing two filed. These two will be required to get the corresponding id which will act as the foreign key. The name of
    this two field must be same.
        role : expects a filed name 'role' having the user roles like Admin/ Suppot. using this a query will be perfomred to RolesAndPermission table 
               to get the corresponding id. Then the corresponding id will be stored as a foreign key.
        theme : expects a field name 'theme' having the theme name like Dark/Night. like role this will be used to perform query theme table to 
                get the corresponding id which will be added to the settings table as foreign key.
    Note: Before inserting the values please make sure, keys which will act as foreign key having proper data in their corresponding table.
    '''

    try: 
        setting_values = Settings.objects.get(pk = setting_id)
    except :
        return Response({'message': 'This value does not exist'})

    if(request.method == "GET"):
        setting_serializer_value = SettingsSerializer(setting_values, many=False)
        return Response (setting_serializer_value.data)

    elif(request.method == "POST"):
        # role = request.data['role']
        # theme = request.data['theme']
        try:
            # role_id = RolesPermissions.objects.filter(roleType= role).values('id')
            # theme_id = Theme.objects.filter(name = theme).values('id')
           
            # settings_values = {'tax': request.data['tax'], 'vat': request.data['vat'], 'role_id': '2', 'point_value': request.data['point_value'],
            # 'point_converted_value':request.data['point_converted_value'],'theme_id': '3'}
            settings_serializers_value = SettingsSerializer (setting_values,data= request.data)
            if(settings_serializers_value.is_valid()):
                settings_serializers_value.save()
                return Response (settings_serializers_value.data, status=status.HTTP_201_CREATED)
            return Response (settings_serializers_value.errors)
        except:
            return Response({'message': 'Setting values could not be updated'})

# ------------------------------- FAQ --------------------------------------

@api_view (["GET","POST"])
def Faq_insertion (request):
    '''
    This method is for inserting frequently ask questions. It has only post response. Calling http://127.0.0.1:8000/site/insert_faq/ will cause to invoke
    this Api. 
    Fileds:
        'question' : This is CharField. This filed will contain the frequently asked question.
        'ans' : This is also a CharField. This filed will contain the answear of the specific question. In both case admin will have the access 
                to add the frequently asking questions and their corresponding answear.
    Expected Post Response:
        {
            "question" : "any question"
            "ans" : "Ans of that corresponding question"
        }
    Successful Post Response:
        {
            "id": 6,
            "question": "What is the return policy",
            "ans": "Thank you for you question. You have to contact within 3 days to our support team.",
            "date": "2020-08-30"
        }
    '''
    if request.method == 'POST':
        try:
            faq_value = FaqSerializer (data= request.data)
            if(faq_value.is_valid()):
                faq_value.save()
                return Response (faq_value.data, status=status.HTTP_201_CREATED)
            return Response (faq_value.errors)
        except:
            return Response({'message': 'It occurs some problem to insert values'})


@api_view (["GET","POST"])
def show_all_Faq (request):
    '''
    This method is for showing all the frequently asked question and their corresponding answear. Calling http://127.0.0.1:8000/site/show_faq/ will 
    cause to invoke this Api. This Api has just Get response.

    Expected data from successful GET Response:
        [
            {
                "id": 2,
                "question": "How is the day?",
                "ans": "Brilliant",
                "date": "2020-08-30"
            },
            {
                "id": 1,
                "question": "Our general rules",
                "ans": "Will be updated very soon",
                "date": "2020-08-30"
            },
            {
                "id": 6,
                "question": "What is the return policy",
                "ans": "Thank you for you question. You have to contact within 3 days to our support team.",
                "date": "2020-08-30"
            }
        ]
    '''
    try:
        if request.method == 'GET':
            faq_value= FAQ.objects.all()
            faq_serializer_value = FaqSerializer (faq_value, many = True)
            return Response (faq_serializer_value.data)
    except:
        return Response({'message': 'It occurs some problem to show the values'})


@api_view (["GET","POST"])
def specific_faq (request,faq_id):
    '''
    This is for updating a particular question or answear. The id of that specific question must need to be sent through parameter to get acess 
    the request data. Calling http://127.0.0.1:8000/site/specific_faq/1/ will cause to invoke this particular Api. It has both get and post response. 
    Successful Get response will provide the stored information correspond to the requested id and through post response the data will be updated.

    Unsuccessful get Response:
        {
            "message": "It occurs some problem"
        }
    Successful Get Response:
        {
            "id": 1,
            "question": "Our general rules",
            "ans": "Will be updated very soon",
            "date": "2020-08-30"
        }
    After updating Successful Post Response:
        {
            "id": 1,
            "question": "Our general rules",
            "ans": "Please follow our general terms and conditions.",
            "date": "2020-08-30"
        }
    '''
    try:
        faq_value= FAQ.objects.get(pk=faq_id)
    except:
        return Response({'message': 'It occurs some problem'})

    if request.method == 'GET':
        faq_serializer_value = FaqSerializer (faq_value, many = False)
        return Response (faq_serializer_value.data)

    if request.method == 'POST':
        try:
            faq_serializer_value = FaqSerializer (faq_value,data= request.data)
            if(faq_serializer_value.is_valid()):
                faq_serializer_value.save()
                return Response (faq_serializer_value.data, status=status.HTTP_201_CREATED)
            return Response (faq_serializer_value.errors)
        except:
            return Response({'message': 'This value could not be updated'})
    

@api_view (["GET","POST"])
def delete_specific_faq (request,faq_id):
    '''
    This is for deleting a particular faq. The value will be deleted through the post response To delete the faq, id of the particular data must need 
    to be sent. Calling http://127.0.0.1:8000/site/delete_faq/2/ will cause to invoke this Api.

    Successful Post Response:
        {
            "message": "The value has been deleted successfully"
        }
    
    Unsuccessful Post Response:
        {
            "message": "It occurs some problem"
        }

    '''
    try:
        faq_value= FAQ.objects.get(pk=faq_id)
    except:
        return Response({'message': 'It occurs some problem'})

    if request.method == 'POST':
        faq_value.delete()
        return Response({'message': 'The value has been deleted successfully'})



@api_view (["GET","POST"])
def insert_contact (request):
    
    if request.method == 'POST':
        try:
            contact_value = ContactUsSerializer (data= request.data)
            if(contact_value.is_valid()):
                contact_value.save()
                return Response ({
                    'success': True,
                    'message': 'Data has been inserted successfully',
                    'data':contact_value.data
                    }, status=status.HTTP_201_CREATED)
            return Response ({
                'success': False,
                'message': 'Data could not record',
                'error':contact_value.errors
                })
        except:
            return Response({
                'success': False,
                'message': 'It occurs some problem to insert values',
                'data': ''
                })


@api_view (["GET","POST"])
def get_all_contact (request):
    
    try:
        contact_value= ContactUs.objects.all()
    except:
        return Response({
            'success':False,
            'message': 'Some internal problem occurs',
            'data': ''
            })

    if request.method == 'GET':
        contact_serializer_value = ContactUsSerializer(contact_value, many = True)
        return Response ({
            'success': True,
            'message':'Value has been retrieved successfully',
            'data':contact_serializer_value.data
            })



@api_view (["GET","POST"])
def delete_specific_contactUs (request,contact_id):

    try:
        contact_value= ContactUs.objects.get(pk=contact_id)
    except:
        return Response({
            'success': False,
            'message': 'It occurs some problem',
            'data': ''
            })

    if request.method == 'POST':
        contact_value.delete()
        return Response({
            'success': True,
            'message': 'The value has been deleted successfully'
            })


@api_view (["GET","POST"])
def get_all_unattended_contact (request):
    
    try:
        contact_value= ContactUs.objects.filter(is_attended = False)
    except:
        return Response({
            'success':False,
            'message': 'It occurs some problem',
            'data': ''
            })

    if request.method == 'GET':
        contact_serializer_value = ContactUsSerializer(contact_value, many = True)
        return Response (
            {
                'success': True,
                'message': 'Value has been retrived successfully.',
                'data':contact_serializer_value.data
            })

@api_view (["GET","POST"])
def admin_attend_contact (request,contact_id):
    
    try:
        contact_value= ContactUs.objects.get(pk=contact_id)
    except:
        return Response({'message': 'It occurs some problem'})

    if request.method == 'GET':
        contact_serializer_value = ContactUsSerializer (contact_value, many = False)
        return Response (contact_serializer_value.data)

    if request.method == 'POST':
        try:
            if not contact_value.is_attended:
                contact_value.is_attended = True
                contact_value.save()
                return Response({
                    'success': True,
                    'message': 'Thank you for attending'
                    })
            else:
                return Response({
                    'success': False,
                    'message': 'You have already attended this.'
                })
        except:
            return Response({
                'success': False,
                'message': 'Some problems while attending'
                })
