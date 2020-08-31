from django.shortcuts import render
from django.http import HttpResponse
from django.http.response import JsonResponse
from rest_framework.parsers import JSONParser 
from rest_framework import status
import datetime
 
from Intense.models import Product,Order,OrderDetails,ProductPrice,Userz,BillingAddress,ProductPoint,ProductSpecification,user_relation,Cupons,Comment,CommentReply,Reviews
from Product_details.serializers import ProductPriceSerializer,ProductPointSerializer,ProductSpecificationSerializer,ProductDetailSerializer,CupponSerializer
from rest_framework.decorators import api_view 
from django.views.decorators.csrf import csrf_exempt
from datetime import datetime
from datetime import timedelta  
from django.utils import timezone
import requests
from django.urls import reverse,reverse_lazy
from django.http import HttpResponseRedirect
from django.conf import settings
from colour import Color
from rest_framework.response import Response



@api_view(['POST',])
def add_points(request):

	if request.method == 'POST':
		pointserializer = ProductPointSerializer(data=request.data)
		if pointserializer.is_valid():
			pointserializer.save()
			return JsonResponse(pointserializer.data, status=status.HTTP_201_CREATED)
		return JsonResponse(pointserializer.errors)


#This updates the product points
@api_view(['POST',])
def update_points(request,product_id):

	try:
		product = ProductPoint.objects.filter(product_id=product_id).last()

		if request.method == 'POST':
			pointserializer = ProductPointSerializer(product,data=request.data)
			if pointserializer.is_valid():
				pointserializer.save()
				return JsonResponse(pointserializer.data, status=status.HTTP_201_CREATED)
			return JsonResponse(pointserializer.errors)

	except ProductPoint.DoesNotExist:
		return JsonResponse({'message': 'This product does not exist'}, status=status.HTTP_404_NOT_FOUND)




#This updates the product points
@api_view(['POST',])
def delete_points(request,product_id):

	try:
		product = ProductPoint.objects.filter(product_id=product_id)

		if request.method == 'POST':
			product.delete()


			return JsonResponse({'message': 'The product points have been deleted'})

	except ProductPoint.DoesNotExist:
		return JsonResponse({'message': 'This product does not exist'}, status=status.HTTP_404_NOT_FOUND)



#This adds the current product price
@api_view(['POST',])
def add_price(request):

	if request.method == 'POST':
		pointserializer = ProductPriceSerializer(data=request.data)
		if pointserializer.is_valid():
			pointserializer.save()
			return JsonResponse(pointserializer.data, status=status.HTTP_201_CREATED)
		return JsonResponse(pointserializer.errors)


#This updates the current product price
@api_view(['POST',])
def update_price(request,product_id):

	try:
		product = ProductPrice.objects.filter(product_id=product_id).last()

		if request.method == 'POST':
			pointserializer = ProductPriceSerializer(product,data=request.data)
			if pointserializer.is_valid():
				pointserializer.save()
				return JsonResponse(pointserializer.data, status=status.HTTP_201_CREATED)
			return JsonResponse(pointserializer.errors)

	except ProductPrice.DoesNotExist:
		return JsonResponse({'message': 'This product does not exist'}, status=status.HTTP_404_NOT_FOUND)




#This updates the product points
@api_view(['POST',])
def delete_price(request,product_id):

	try:
		product = ProductPrice.objects.filter(product_id=product_id)

		if request.method == 'POST':
			product.delete()


			return JsonResponse({'message': 'The product prices have been deleted'})

	except ProductPoint.DoesNotExist:
		return JsonResponse({'message': 'This product does not exist'}, status=status.HTTP_404_NOT_FOUND)


#This adds product points 
@api_view(['POST',])
def add_specification(request):

	arr={
		"product_id":12,
		"weight": 17,
		"color":["red","blue","orange"],
		"unit":["kg","gram"],
		"size":["medium","small"]     
		}

	if request.method == 'POST':
		#color = request.data.get('color')
		#colorhex = Color(color).hex
		#size = request.data.get('size')
		#unit = request.data.get('unit')
		#weight = request.data.get('weight')


		#product_spec = ProductSpecification.objects.create(color=colorhex,size = size , unit=unit,weight=weight)
		#product_spec.save()
		#print(product_spec.color)
		pointserializer = ProductSpecificationSerializer(data=arr)

		if pointserializer.is_valid():
			pointserializer.save()
			return JsonResponse(pointserializer.data, status=status.HTTP_201_CREATED)
		return Response (pointserializer.errors)


#This updates the latest product specification
@api_view(['POST',])
def update_specification(request,product_id):

	arr={
		"weight": 18,
		"color":["red","blue","orange","green","black"],
		"unit":["kg","gram"],
		"size":["medium"]     
		}

	try:
		product = ProductSpecification.objects.filter(product_id=product_id).last()

		if request.method == 'POST':
			pointserializer = ProductSpecificationSerializer(product,data=arr)
			if pointserializer.is_valid():
				pointserializer.save()
				return JsonResponse(pointserializer.data, status=status.HTTP_201_CREATED)
			return Response (pointserializer.errors)

	except ProductPoint.DoesNotExist:
		return JsonResponse({'message': 'This product does not exist'}, status=status.HTTP_404_NOT_FOUND)




#This deletes the product specification
@api_view(['POST',])
def delete_specification(request,product_id):

	try:
		product = ProductSpecification.objects.filter(product_id=product_id)

		if request.method == 'POST':
			product.delete()


			return JsonResponse({'message': 'The product specification have been deleted'})

	except ProductPoint.DoesNotExist:
		return JsonResponse({'message': 'This product does not exist'}, status=status.HTTP_404_NOT_FOUND)


@api_view(['GET',])
def show_specification(request,product_id):

	try:
		product = ProductSpecification.objects.filter(product_id=product_id)
		productserializer = ProductSpecificationSerializer(product,many=True)
		return JsonResponse(productserializer.data,safe=False)

	except Product.DoesNotExist:
		return JsonResponse({'message': 'This Product does not exist'}, status=status.HTTP_404_NOT_FOUND)



@api_view(['GET',])
def show(request,product_id):

	#url = reverse('product_price_point_specification:showspec',args=[product_id])
	#data= requests.get(url)
	#url= reverse('product_price_point_specification:showspec',args=[product_id])
	#main = str(settings.BASE_DIR) + url
	#print(main)
	#data = requests.get(main)
	url=request.build_absolute_uri(reverse('product_price_point_specification:showspec',args=[product_id]))
	#print("------")
	#print(url)
	data= requests.get(url)
	return HttpResponse(data)																																								
	

#This changes the comments,replies,reviews and order tables
@api_view(['POST',])
def transfer(request,user_id):
	# Here userid provided is the newly verified userid 
	try:
	
		existing_user = user_relation.objects.filter(verified_user_id=user_id).last()
		print(existing_user)

	except:
		existing_user = None

	if existing_user is not None:
		#Change the ids in the certain table

		# print(type(existing_user.verified_user_id))
		# print(existing_user.non_verified_user_id)
		user_id = existing_user.verified_user_id
		non_verified_user_id = existing_user.non_verified_user_id
	
		
		#Update all the order tables

		orders = Order.objects.filter(non_verified_user_id = non_verified_user_id).update(user_id=user_id,non_verified_user_id=None)
        
        #Update the Billing address

		billing_address = BillingAddress.objects.filter(non_verified_user_id=non_verified_user_id).update(user_id=user_id,non_verified_user_id=None)

		#Update the comment,reply and review tables

		comments = Comment.objects.filter(non_verified_user_id=non_verified_user_id).update(user_id=user_id,non_verified_user_id=None)
		reply = CommentReply.objects.filter(non_verified_user_id=non_verified_user_id).update(user_id=user_id,non_verified_user_id=None)
		reviews = Reviews.objects.filter(non_verified_user_id=non_verified_user_id).update(user_id=user_id,non_verified_user_id=None)
         
		return JsonResponse({'message': 'The user does exist'})
			
	else:
		return JsonResponse({'message': 'The user does not exist'})



@api_view(['GET',])
def product_detail(request,product_id):

	try:
		product = Product.objects.filter(id=product_id).last()

	except:
		product = None

	if product is not None:

		product_serializer = ProductDetailSerializer(product,many=False)
		return JsonResponse(product_serializer.data,safe=False)

	else:
		return JsonResponse({'message': 'This product does not exist'})


# --------------------------------- Product Cupon -------------------------------

@api_view(["GET","POST"])
def insert_cupon(request):
    '''
    This is for inserting cupon code into the databse. Admin will set the cupon code and it will apear to the users while buying a product.
    Calling http://127.0.0.1:8000/cupons/create_cupon/ will cause to invoke this Api. This Api just have Post response.

    Post Response:
        cupon_code : This is a character field. This will be cupon named after the inserting name value.
        amount : This will be the amount which will be deducted from the user payable balance.
        start_from: This is DateField. It will be created automatically upon the creation of a cupon.
        valid_to: This is another DateField. While creating a cupon admin will set the date.
        is_active : This is a BooleanField. This will indicate wheather the cupon is active or not. Using this data, cupon can be deactivated before ending
                    the validation time. 

    '''
    if(request.method == "POST"):
        serializers = CupponSerializer (data= request.data)
        if(serializers.is_valid()):
            serializers.save()
            return Response (serializers.data, status=status.HTTP_201_CREATED)
        return Response (serializers.errors)

@api_view(["GET","POST"])
def get_all_cupons(request):
    '''
    This is for getting all the cupons. Calling http://127.0.0.1:8000/cupons/all_cupon/ will cause to invoke this Api. 
    The Get Response will return following structured datas.

    Get Response:
        [
            {
                "id": 2,
                "cupon_code": "30% Off",
                "amount": 50.0,
                "start_from": "2020-08-27",
                "valid_to": "2020-09-30",
                "is_active": false
            },
            {
                "id": 3,
                "cupon_code": "25 Taka Off",
                "amount": 25.0,
                "start_from": "2020-08-27",
                "valid_to": "2020-10-27",
                "is_active": false
            }
        ]
    '''
    if(request.method == "GET"):
        queryset = Cupons.objects.all()
        serializers = CupponSerializer (queryset,many = True)
        return Response (serializers.data)

@api_view(["GET","POST"])
def update_specific_cupons(request,cupon_id):
    '''
    This is for updating a particular cupon. Calling http://127.0.0.1:8000/cupons/update_cupon/4/ will cause to invoke this Api.
    While calling this Api, as parameters cupon id must need to be sent.

    After updating expected Post Response:
        {
            "id": 4,
            "cupon_code": "25 Taka Off",
            "amount": 25.0,
            "start_from": "2020-08-27",
            "valid_to": "2020-10-27",
            "is_active": true
        }
    '''

    try: 
        cupon = Cupons.objects.get(pk = cupon_id)
    except :
        return Response({'Message': 'Check wheather requested data exists or not'})

    if(request.method == "GET"):
        cupon_serializer = CupponSerializer(cupon, many=False)
        return Response (cupon_serializer.data)

    elif(request.method == "POST"):
        Cupon_serializers = CupponSerializer( cupon, data= request.data)
        if(Cupon_serializers.is_valid()):
            Cupon_serializers.save()
            return Response (Cupon_serializers.data, status=status.HTTP_201_CREATED)
        return Response (Cupon_serializers.errors)

@api_view(["GET","POST"])
def delete_specific_cupons(request,cupon_id):
    '''
    This is for deleting a particular cupon value. Calling 127.0.0.1:8000/cupons/delete_cupon/4/ will cause to invoke this Api.
    After performing delete operation successfully this api will provide following response.

    Successful Post Response:
        [
            "Cupon has been deleted successfully"
        ]
    Unsuccessful Post Response:
        {
            "Message": "Some internal problem occurs while deleting the value"
        }
    '''

    try: 
        cupon = Cupons.objects.get(pk = cupon_id)
    except :
        return Response({'Message': 'Some internal problem occurs while deleting the value'})

    if(request.method == "POST"):
        cupon.delete()
        return Response({'Cupon has been deleted successfully'})

	