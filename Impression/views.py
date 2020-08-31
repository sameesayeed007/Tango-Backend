from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
import datetime
from Intense.models import ProductImpression
from .serializers import ProductImpressionSerializer,userImpressionSerializer,ClickImpressionSerializer,ViewImpressionSerializer,CartImpressionSerializer,SalesImpressionSerializer
import requests


@api_view (["GET","POST"])
def get_specific_product_impression (request, product_id):
    '''
    This Api is for getting the impression of a particular product id. To access a particular product improssion, in url the particlar product id
    is required to provide as a parameter. Calling http://127.0.0.1:8000/impress/get_specific/19 this will cause to invoke this API.
    This API just have Get response.

    GET Reponse:
        In Get response following data will be provided through this API.

        Users : (This is an integer array filed. This filed will provide user id, who at least once had attention on this particular product.In the value
                there might be some negetive value like (-1) which represents no user id [Just ignore those ids].)

        product_id: (This is the product id based on which the impression has been retrived)
        view_count : (This will be an integer value. It will return how much time this particular product was viewed by the user)
        click_count : (This will provide an integer value which represents how much time this particular product was clicked)
        car_count : (This will also return an integer value. This value represents how much time this particular product was added into the cart)
        sales_count : (Like others it is also an integer field. This value represnts how many times this product was sold.)
        dates : (This is a normal date and time field. It returns the date and time on which the particular product impression has been created.)
    '''

    if request.method == 'GET':
        try:
            queryset = ProductImpression.objects.get(product_id = product_id)
            impression_serializers = ProductImpressionSerializer (queryset, many = False)
            return Response (impression_serializers.data)
        except:
            return Response({'message': 'Thre is no value to retrieve'})


@api_view (["GET","POST"])
def insert_product_impression (request):
    '''
    This Api is for inserting the values into the impression table. This api assumes there will be two types of user one is normal verified user
    and another one is non verified means guest user. Considering the both user this Api has been developed. This Api just have post request and
    while performing the post request it expects few data from the sender. Calling http://127.0.0.1:8000/impress/post_value/ this url will cause to 
    invoke this API.

    POST Response:
    This Api expects the following data while performing the Post response.
        product_id : (This is an ineteger value. While performing the post request the user must need to provide the product id. It can not be null)
        Users: (This filed stores user id who had impression on a particular product at least once. This is an array field but while sending the data 
                user may send and empty data or data as json object.)
        view_count : (This field stores the view count data. This is an integer value and may come from front end or others. It expects either a positive 
                    number or zero as a Json response.)
        click_count : (Like the view count it also expects either zero value or a positive inetger value as Json response)
        cart_count : (It also expects either zero or a positive value as response)
        sales_count :(Like others it also expects some positive values or zero as json response)
        non_verified_user : (As our assusmption is there will be two types of user either verified or guest. For the guest user, the user id who had 
                            interest at least once in this particular product will be stored. This is an integer array field. Non verified user id 
                            is expected in response.)
    '''
    # demo values
    api_values = {'product_id': '20','Users': '', 'view_count' : '0', 'click_count': '1', 'cart_count' : '0', 'sales_count' : '1', 'non_verified_user' : '3'}


    if request.method == 'POST':

        product = ProductImpression.objects.filter(product_id = api_values['product_id']).first()
        if product is None:
            if api_values['Users'] == '':
                api_values['Users'] = [-1]
            else:
                api_values['Users'] = [int(api_values['Users'])]
            
            if api_values['non_verified_user'] == '':
                api_values['non_verified_user'] = [-1]
            else:
                api_values['non_verified_user'] = [int(api_values['non_verified_user'])]

            serializer_value = ProductImpressionSerializer (data= api_values)
            if(serializer_value.is_valid()):
                serializer_value.save()
                return Response (serializer_value.data, status=status.HTTP_201_CREATED)
            return Response (serializer_value.errors)
            
        else:
            if api_values['Users'] == '':
                product.Users.append(-1)
            else:
                product.Users.append(int(api_values['Users']))
            
            if api_values['non_verified_user'] == '':
                product.non_verified_user.append(-1)
            else:
                product.non_verified_user.append(int(api_values['non_verified_user']))
            
            product.view_count = product.view_count+ int(api_values['view_count'])
            product.click_count = product.click_count+ int(api_values['click_count'])
            product.cart_count = product.cart_count+ int(api_values['cart_count'])
            product.sales_count = product.sales_count+ int(api_values['sales_count'])
            
            product_val = product.__dict__
            serializer_value = ProductImpressionSerializer (product,data= product_val)
            if(serializer_value.is_valid()):
                serializer_value.save()
                return Response (serializer_value.data, status=status.HTTP_201_CREATED)
            return Response (serializer_value.errors)
            
@api_view (["GET","POST"])
def delete_specific_product_impression (request, product_id):
    '''
    This Api is for deleting a particular product impression. When a product will be deleted from the table, impression of this particular product is 
    also will need to delete. Here, particular product id based on which the product impression will be deleted is required to pass as parameter. 
    calling http://127.0.0.1:8000/impress/delete_specific/19 will cause to invoke this Api. The delete operation will perform user the post request.
    '''

    try: 
        specific_impress = ProductImpression.objects.get(product_id = product_id)
    except :
        return Response({'message': 'There is no value to delete'})
    
    if request.method == "POST":
        specific_impress.delete()
        return Response({'message': ' Value is successfully  deleted'}, status=status.HTTP_204_NO_CONTENT)


@api_view (["GET","POST"])
def get_impression_user_id (request, product_id):
    '''
    This Api is for getting the both verified and non verified users who had interest on this partiicular product. 
    Calling http://127.0.0.1:8000/impress/get_user_impress/19 will cause to invoke this Api. This Api just have Get Response.

    Get Response:
        In Get response this Api will send a Json object including the following fields.
        verified_user_data : (This will be an array. Retured array data represnts the verified user ids)
        non_verified_user_data : (This will also be an array field. This data represents the non verified users id who had at least once 
                                interest on this particular product.)
        product_id : (For which product_id the impression datas are.)
        dates : This is the date when the particular product impression was created.
    '''

    if request.method == 'GET':
        try:
            queryset = ProductImpression.objects.get(product_id = product_id)
            impression_serializers = userImpressionSerializer (queryset)
            return Response (impression_serializers.data)
        except:
            return Response({'message': 'There is no value to Show'})

@api_view (["GET","POST"])
def get_click_impression (request, product_id):
    '''
    This Api is for getting the click impression of a  partiicular product. Calling http://127.0.0.1:8000/impress/get_click_impress/19 
    will cause to invoke this Api. This Api just have Get Response.

    Get Response:
        In Get response this Api will send a Json object including the following fields.
        click_impression : (This will be an integer value. This data represnts how many times this particular product was being clicked.)
        product_id : (For which product_id the impression datas are.)
        dates : This is the date when the particular product impression was created.
    '''

    if request.method == 'GET':
        try:
            queryset = ProductImpression.objects.get(product_id = product_id)
            click_impression_serializers = ClickImpressionSerializer (queryset)
            return Response (click_impression_serializers.data)
        except:
            return Response({'message': 'There is no value to Show'})

@api_view (["GET","POST"])
def get_view_impression (request, product_id):
    '''
    This Api is for getting the view impression of a  partiicular product. Calling http://127.0.0.1:8000/impress/get_view_impress/19 
    will cause to invoke this Api. This Api just have Get Response.

    Get Response:
        In Get response this Api will send a Json object including the following fields.
        view_impression : (This will be an integer value. This data represnts how many times this particular product was being viewed.)
        product_id : (For which product_id the impression datas are.)
        dates : This is the date when the particular product impression was created.
    '''

    if request.method == 'GET':
        try:
            queryset = ProductImpression.objects.get(product_id = product_id)
            view_impression_serializers = ViewImpressionSerializer (queryset)
            return Response (view_impression_serializers.data)
        except:
            return Response({'message': 'There is no value to Show'})
        

       
@api_view (["GET","POST"])
def get_cart_impression (request, product_id):
    '''
    This Api is for getting the cart impression of a  partiicular product. Calling http://127.0.0.1:8000/impress/get_cart_impress/19 
    will cause to invoke this Api. This Api just have Get Response.

    Get Response:
        In Get response this Api will send a Json object including the following fields.
        cart_impression : (This will be an integer value. This data represnts how many times this particular product was being added into the cart.)
        product_id : (For which product_id the impression datas are.)
        dates : This is the date when the particular product impression was created.
    '''

    if request.method == 'GET':
        try:
            queryset = ProductImpression.objects.get(product_id = product_id)
            cart_impression_serializers = CartImpressionSerializer (queryset)
            return Response (cart_impression_serializers.data)
        except:
            return Response({'message': 'There is no value to Show'})


@api_view (["GET","POST"])
def get_sales_impression (request, product_id):
    '''
    This Api is for getting the sales impression of a  partiicular product. Calling http://127.0.0.1:8000/impress/get_sales_impress/19 
    will cause to invoke this Api. This Api just have Get Response.

    Get Response:
        In Get response this Api will send a Json object including the following fields.
        sales_impression : (This will be an integer value. This data represnts how many times this particular product was being sold.)
        product_id : (For which product_id the impression datas are.)
        dates : This is the date when the particular product impression was created.
    '''

    if request.method == 'GET':
        try:
            queryset = ProductImpression.objects.get(product_id = product_id)
            cart_impression_serializers = SalesImpressionSerializer (queryset)
            return Response (cart_impression_serializers.data)
        except:
            return Response({'message': 'There is no value to Show'})