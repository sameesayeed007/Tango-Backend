from django.shortcuts import render
from django.http import HttpResponse
from django.http.response import JsonResponse
from rest_framework.parsers import JSONParser 
from rest_framework import status
import datetime
 
from Intense.models import Product,Order,OrderDetails,ProductPrice,Userz,BillingAddress,ProductPoint,discount_product,ProductImpression,Profile,Cupons,ProductSpecification,CompanyInfo

from Cart.serializers import ProductSerializer, OrderSerializer,OrderSerializerz,OrderSerializerzz,OrderDetailsSerializer,ProductPriceSerializer,UserzSerializer,BillingAddressSerializer,ProductPointSerializer
from Product_details.serializers import ProductImpressionSerializer,ProductSpecificationSerializer
from rest_framework.decorators import api_view 
from django.views.decorators.csrf import csrf_exempt
from datetime import datetime
from datetime import timedelta  
from django.utils import timezone


# Create your views here.
@api_view(['PUT',])
def add_cart(request,productid):

	user_id = request.data.get('user_id')
	non_verified_user_id = request.data.get('non_verified_user_id')
	quantity = request.data.get('quantity')
	color = request.data.get('color')
	size = request.data.get('size')
	#unit = request.data.get('unit')
	quantity = int(quantity)
	if user_id is not None:
		user_id = int(user_id)
		non_verified_user_id =0

	else:
		non_verified_user_id = int(non_verified_user_id)
		user_id = 0

		#Fetching the specific product info
	p_price=0
	p_discount=0
	p_point = 0
	total_price=0 
	total_point=0
	p_name=""
	unit_point = 0
	unit_price = 0
	#Fetching the product points
	try:
		product_point = ProductPoint.objects.filter(product_id=productid).last()
	except:
		product_point = None

	if product_point is not None:

		if product_point.point:
			p_point = product_point.point

		else:
			p_point = 0
		current_date = timezone.now().date()
		start_date = current_date
		end_date = current_date
		

		if product_point.start_date:
			start_date = product_point.start_date
		else:
			start_date = current_date

		if product_point.end_date:
			end_date = product_point.end_date

		else:
			end_date = current_date


		if (current_date >= start_date) and (current_date <= end_date):
			total_point = p_point * quantity
			unit_point = p_point

		else:
			total_point = 0
			unit_point = 0

	else:
		
		total_point = 0
		unit_point = 0

	#Fetching the product price
	try:

		product_price = ProductPrice.objects.filter(product_id=productid).last()
	except:
		product_price = None

	if product_price is not None:
		p_price = product_price.price
		unit_price = p_price
	else:
		p_price = 0
		unit_price = p_price

	#Fetching the product discount
	try:
		product_discount = discount_product.objects.filter(product_id=productid).last()
	except:
		product_discount = None

	if product_discount is not None:
		if product_discount.amount:
			p_discount = product_discount.amount
		else:
			p_discount = 0
		current_date = timezone.now().date()
		discount_start_date = current_date
		discount_end_date = current_date
		if product_discount.start_date:

			discount_start_date = product_discount.start_date
		else:
			discount_start_date = current_date

		if product_discount.end_date:
			discount_end_date = product_discount.end_date

		else:
			discount_end_date = current_date

		

		if (current_date >= discount_start_date) and (current_date <= discount_end_date):
			total_discount = p_discount * quantity
			total_price = (p_price * quantity) - total_discount
			unit_price = p_price - p_discount

		else:
			total_discount=0
			total_price = (p_price * quantity) - total_discount
			unit_price = p_price
	else:
		total_price = p_price * quantity
		unit_price = p_price



	try:
		product_name = Product.objects.filter(id=productid).last()
	except:
		product_name = None

	if product_name is not None:

		p_name = str(product_name.title)
		p_id = product_name.id
		

	else:
		p_name = ""

	try:
		product_impression = ProductImpression.objects.filter(product_id=productid)[0:1].get()
	except:
		product_impression = None

	if product_impression is None:
		#Create a productimpression object for that particular product
		print("create impression")
		p_impression = ProductImpression.objects.create(product_id=productid)
		p_impression_serializer = ProductImpressionSerializer(p_impression,data=request.data)
		if p_impression_serializer.is_valid():
			p_impression_serializer.save()

	else:
		product_impression = ProductImpression.objects.filter(product_id=productid)[0:1].get()

		

	


	if non_verified_user_id == 0:


		#checking if the user exists in product impression
		try:
			product_impression = ProductImpression.objects.filter(product_id=productid)[0:1].get()
		except:
			product_impression = None

		if product_impression:
			users_list = product_impression.users
			cart_count = product_impression.cart_count
			if user_id in users_list:
				pass
			else:
				users_list.append(user_id)

			cart = cart_count + quantity
			ProductImpression.objects.filter(product_id=productid).update(users=users_list,cart_count=cart)



		

		try:
			#Fetching the specific order of the specific user that hasnt been checked out
			specific_order = Order.objects.filter(user_id=user_id,checkout_status=False)[0:1].get()
			order_id = specific_order.id

		except:
			specific_order = None

		    # if the specific user order exists
		if specific_order is not None:
			
			
			try:
				#checking if the product exists in this order
				specific_order_product = OrderDetails.objects.filter(order_id =order_id , product_id=productid,is_removed=False,product_color=color,product_size=size)[0:1].get()
			except:
				specific_order_product = None
			
			orderserializers = OrderSerializer(specific_order, data=request.data)

			if orderserializers.is_valid():
				orderserializers.save()
		        

			if specific_order_product is not None:
				
				specific_order_product.total_quantity += quantity
				specific_order_product.remaining += quantity
				specific_order_product.total_price += total_price
				specific_order_product.total_point += total_point
				# specifc_order_product.product_color.append(color)
				# specifc_order_product.product_size.append(size)
				# specifc_order_product.product_unit.append(unit)
				specific_order_product.save()
				orderdetailsserializers = OrderDetailsSerializer(specific_order_product , data=request.data)
				if orderdetailsserializers.is_valid():
					orderdetailsserializers.save()
					return JsonResponse({'success':True ,'message':'The quantity has been updated'})
				else:
					return JsonResponse(orderdetailsserializers.errors)


			else:
				#create a new orderdetail for that order id if the product is bough for the first time
				# product_color = [color]
				# product_size = [size]
				# product_color = [unit]

				orderdetails = OrderDetails.objects.create(order_id = order_id , product_id=productid,quantity=quantity,total_quantity=quantity,remaining=quantity,unit_price=unit_price,unit_point=unit_point,total_price=total_price,total_point=total_point,product_name=p_name,product_color=color,product_size=size)
				
				orderdetails.save()
				orderdetailsserializer = OrderDetailsSerializer(orderdetails , data=request.data)
				if orderdetailsserializer.is_valid():
					orderdetailsserializer.save()
					return JsonResponse({'success':True ,'message':'The product has been added to your cart'})
				else:
					return JsonResponse(orderdetailsserializers.errors)
				
		# if no order for the user exists
		else:
			

			#create a new Order 
			order = Order.objects.create(user_id = user_id)
			order.save()
			orderserializer = OrderSerializer(order , data=request.data)
			if orderserializer.is_valid():
				orderserializer.save()
			else:
				return JsonResponse(orderserializer.errors)

			
			#create a new order details for the specific product for the specific order
			orderdetails = OrderDetails.objects.create(order_id = order.id , product_id=productid,quantity=quantity,total_quantity=quantity,remaining=quantity,unit_price=unit_price,unit_point=unit_point,total_price=total_price,total_point=total_point,product_name=p_name,product_color=color,product_size=size)
		
			orderdetails.save()
			orderdetailserializer = OrderDetailsSerializer(orderdetails, data=request.data)
			if orderdetailserializer.is_valid():
				orderdetailserializer.save()
				return JsonResponse({'success':True,'message':'A new order with a order details has been created'})
			else:
				return JsonResponse(orderdetailserializer.errors)

						

	else:

        #checking if the user exists in the impression user list
		try:
			product_impression = ProductImpression.objects.filter(product_id=productid)[0:1].get()
		except:
			product_impression = None
		if product_impression:
			users_list = product_impression.non_verified_user
			cart_count = product_impression.cart_count
			if non_verified_user_id in users_list:
				pass
			else:
				users_list.append(non_verified_user_id)

			cart = cart_count + quantity
			ProductImpression.objects.filter(product_id=productid).update(non_verified_user=users_list,cart_count=cart)

		try:
			#Fetching the specific order of the specific user that hasnt been checked out
			specific_order = Order.objects.filter(non_verified_user_id=non_verified_user_id,checkout_status=False)[0:1].get()
			order_id = specific_order.id

		except:
			specific_order = None

		    # if the specific user order exists
		if specific_order is not None:
			
			
			try:
				#checking if the product exists in this order
				specific_order_product = OrderDetails.objects.filter(order_id =order_id , product_id=productid,is_removed=False,product_color=color,product_size=size)[0:1].get()
			except:
				specific_order_product = None
			
			orderserializers = OrderSerializer(specific_order, data=request.data)

			if orderserializers.is_valid():
				orderserializers.save()
		        

			if specific_order_product is not None:
				
				specific_order_product.total_quantity += quantity
				specific_order_product.remaining += quantity
				specific_order_product.total_price += total_price
				specific_order_product.total_point += total_point
				specific_order_product.save()
				orderdetailsserializers = OrderDetailsSerializer(specific_order_product , data=request.data)
				if orderdetailsserializers.is_valid():
					orderdetailsserializers.save()
					return JsonResponse({'success':True ,'message':'The quantity has been updated'})
				else:
					return JsonResponse(orderdetailsserializers.errors)


			else:
				#create a new orderdetail for that order id if the product is bough for the first time 
				orderdetails = OrderDetails.objects.create(order_id = order_id , product_id=productid,quantity=quantity,total_quantity=quantity,remaining=quantity,unit_price=unit_price,unit_point=unit_point,total_price=total_price,total_point=total_point,product_name=p_name,product_color=color,product_size=size)
				
				orderdetails.save()
				orderdetailsserializer = OrderDetailsSerializer(orderdetails , data=request.data)
				if orderdetailsserializer.is_valid():
					orderdetailsserializer.save()
					return JsonResponse({'success':True ,'message':'The product has been added to your cart'})
				else:
					return JsonResponse(orderdetailsserializers.errors)
				
		# if no order for the user exists
		else:
			

			#create a new Order 
			order = Order.objects.create(non_verified_user_id = non_verified_user_id)
			order.save()
			orderserializer = OrderSerializer(order , data=request.data)
			if orderserializer.is_valid():
				orderserializer.save()
			else:
				return JsonResponse(orderserializer.errors)

			
			#create a new order details for the specific product for the specific order
			orderdetails = OrderDetails.objects.create(order_id = order.id , product_id=productid,quantity=quantity,total_quantity=quantity,remaining=quantity,unit_price=unit_price,unit_point=unit_point,total_price=total_price,total_point=total_point,product_name=p_name,product_color=color,product_size=size)
		
			orderdetails.save()
			orderdetailserializer = OrderDetailsSerializer(orderdetails, data=request.data)
			if orderdetailserializer.is_valid():
				orderdetailserializer.save()
				return JsonResponse({'success':True,'message':'A new order with a order details has been created'})
			else:
				return JsonResponse(orderdetailserializer.errors)
		




@api_view(['PUT',])
def increase_quantity(request,productid):

	#values = {'user_id':'2', 'non_verified_user_id':''}
	color = request.data.get('color')
	size = request.data.get('size')
	#unit = request.data.get('unit')
	user_id = request.data.get('user_id')
	non_verified_user_id = request.data.get('non_verified_user_id')
	#quantity = request.data.get('quantity')
	#quantity = int(quantity)
	if user_id is not None:
		user_id = int(user_id)
		non_verified_user_id =0

	else:
		non_verified_user_id = int(non_verified_user_id)
		user_id = 0



	p_price=0
	p_discount=0
	p_point = 0
	total_price=0 
	total_point=0
	p_name=""
	unit_point = 0
	unit_price = 0
	quantity = 1
	#Fetching the product points
	try:
		product_point = ProductPoint.objects.filter(product_id=productid).last()
	except:
		product_point = None

	if product_point is not None:
		p_point = product_point.point
		start_date = product_point.start_date
		end_date = product_point.end_date
		current_date = timezone.now().date()

		if product_point.start_date:
			start_date = product_point.start_date
		else:
			start_date = current_date

		if product_point.end_date:
			end_date = product_point.end_date

		else:

			end_date = current_date
		

		if (current_date >= start_date) and (current_date <= end_date):
			total_point = p_point * quantity
			unit_point = p_point

		else:
			total_point = 0
			unit_point = 0

	else:
		
		total_point = 0
		unit_point = 0

	#Fetching the product price
	try:

		product_price = ProductPrice.objects.filter(product_id=productid).last()
	except:
		product_price = None

	if product_price is not None:
		p_price = product_price.price
		unit_price = p_price
	else:
		p_price = 0
		unit_price = p_price

	#Fetching the product discount
	try:
		product_discount = discount_product.objects.filter(product_id=productid).last()
	except:
		product_discount = None

	if product_discount is not None:
		p_discount = product_discount.amount
		discount_start_date = product_discount.start_date
		discount_end_date = product_discount.end_date
		current_date = timezone.now().date()

		if product_discount.start_date:
			discount_start_date = product_discount.start_date
		else:
			discount_start_date = current_date

		if product_discount.end_date:
			discount_end_date = product_discount.end_date

		else:

			discount_end_date = current_date

		if (current_date >= discount_start_date) and (current_date <= discount_end_date):
			total_discount = p_discount * quantity
			total_price = (p_price * quantity) - total_discount
			unit_price = p_price - p_discount

		else:
			total_discount=0
			total_price = (p_price * quantity) - total_discount
			unit_price = p_price
	else:
		total_price = p_price * quantity
		unit_price = p_price



	try:
		product_name = Product.objects.filter(id=productid).last()
	except:
		product_name = None

	if product_name is not None:

		p_name = str(product_name.title)
		p_id = product_name.id
		

	else:
		p_name = ""

	# user_id = values['user_id']
	# non_verified_user_id = values['non_verified_user_id']
	cart_count = 0
    
	try:
		product_impression = ProductImpression.objects.filter(product_id=productid)[0:1].get()
	except:
		product_impression = None

	if product_impression is None:
		pass
	else:

		cart_count = product_impression.cart_count

	cart = cart_count + 1
	ProductImpression.objects.filter(product_id=productid).update(cart_count=cart)



	if non_verified_user_id == 0:

		try:
			#Fetching the specific order of the specific user that hasnt been checked out
			specific_order = Order.objects.filter(user_id=user_id,checkout_status=False)[0:1].get()
			order_id = specific_order.id
		except:
			specific_order = None


		# if the specific user exists
		if specific_order is not None:

			try:
				#checking if the product exists in this order
				specific_order_product = OrderDetails.objects.filter(order_id =order_id , product_id=productid,is_removed=False,product_color=color,product_size=size)[0:1].get()

			except:
				specific_order_product = None

			if specific_order_product is not None:
				

				if specific_order_product.total_quantity >= 1:
					specific_order_product.total_quantity += 1
					specific_order_product.remaining += 1
					specific_order_product.total_price += total_price
					specific_order_product.total_point += total_point
					specific_order_product.save()
					orderdetailsserializers = OrderDetailsSerializer(specific_order_product , data=request.data)
					if orderdetailsserializers.is_valid():
						orderdetailsserializers.save()
						return JsonResponse({'success':True,'message':'The quantity has been increased'})
				

			else:
				return JsonResponse({'success':False,'message':'The item does not exist'})	


		else:
			return JsonResponse({'success':False,'message':'The order does not exist'})

	else:

		try:
			#Fetching the specific order of the specific user that hasnt been checked out
			specific_order = Order.objects.filter(non_verified_user_id=non_verified_user_id,checkout_status=False)[0:1].get()
			order_id = specific_order.id
		except:
			specific_order = None


		# if the specific user exists
		if specific_order is not None:

			try:
				#checking if the product exists in this order
				specific_order_product = OrderDetails.objects.filter(order_id =order_id , product_id=productid,is_removed=False,product_color=color,product_size=size)[0:1].get()

			except:
				specific_order_product = None

			if specific_order_product is not None:

				if specific_order_product.total_quantity >= 1:
					specific_order_product.total_quantity += 1
					specific_order_product.remaining += 1
					specific_order_product.total_price += total_price
					specific_order_product.total_point += total_point
					specific_order_product.save()
					orderdetailsserializers = OrderDetailsSerializer(specific_order_product , data=request.data)
					if orderdetailsserializers.is_valid():
						orderdetailsserializers.save()

						return JsonResponse({'success':True,'message':'The quantity has been increased'})
					


			else:
				return JsonResponse({'success':False,'message':'The item does not exist'})	


		else:
			return JsonResponse({'success':False,'message':'The order does not exist'})





@api_view(['PUT',])
def decrease_quantity(request,productid):

	color = request.data.get('color')
	size = request.data.get('size')
	#unit = request.data.get('unit')

	p_price=0
	p_discount=0
	p_point = 0
	total_price=0 
	total_point=0
	p_name=""
	unit_point = 0
	unit_price = 0
	quantity = 1
	#Fetching the product points
	try:
		product_point = ProductPoint.objects.filter(product_id=productid).last()
	except:
		product_point = None

	if product_point is not None:
		p_point = product_point.point
		start_date = product_point.start_date
		end_date = product_point.end_date
		current_date = timezone.now().date()

		if product_point.start_date:
			start_date = product_point.start_date
		else:
			start_date = current_date

		if product_point.end_date:
			end_date = product_point.end_date

		else:

			end_date = current_date
	

		if (current_date >= start_date) and (current_date <= end_date):
			total_point = p_point * quantity
			unit_point = p_point

		else:
			total_point = 0
			unit_point = 0

	else:
		
		total_point = 0
		unit_point = 0

	#Fetching the product price
	try:

		product_price = ProductPrice.objects.filter(product_id=productid).last()
	except:
		product_price = None

	if product_price is not None:
		p_price = product_price.price
		unit_price = p_price
	else:
		p_price = 0
		unit_price = p_price

	#Fetching the product discount
	try:
		product_discount = discount_product.objects.filter(product_id=productid).last()
	except:
		product_discount = None

	if product_discount is not None:
		p_discount = product_discount.amount
		discount_start_date = product_discount.start_date
		discount_end_date = product_discount.end_date
		current_date = timezone.now().date()

		if product_discount.start_date:
			discount_start_date = product_discount.start_date
		else:
			discount_start_date = current_date

		if product_discount.end_date:
			discount_end_date = product_discount.end_date

		else:

			discount_end_date = current_date

		if (current_date >= discount_start_date) and (current_date <= discount_end_date):
			total_discount = p_discount * quantity
			total_price = (p_price * quantity) - total_discount
			unit_price = p_price - p_discount

		else:
			total_discount=0
			total_price = (p_price * quantity) - total_discount
			unit_price = p_price
	else:
		total_price = p_price * quantity
		unit_price = p_price



	try:
		product_name = Product.objects.filter(id=productid).last()
	except:
		product_name = None

	if product_name is not None:

		p_name = str(product_name.title)
		p_id = product_name.id
		
	else:
		p_name = ""



	user_id = request.data.get('user_id')
	non_verified_user_id = request.data.get('non_verified_user_id')
	if user_id is not None:
		user_id = int(user_id)
		non_verified_user_id =0

	else:
		non_verified_user_id = int(non_verified_user_id)
		user_id = 0

	cart_count = 0
    
	try:
		product_impression = ProductImpression.objects.filter(product_id=productid)[0:1].get()
	except:
		product_impression = None

	if product_impression is None:
		pass
	else:

		cart_count = product_impression.cart_count

	cart = cart_count - 1
	ProductImpression.objects.filter(product_id=productid).update(cart_count=cart)

	if non_verified_user_id == 0:


		try:
			#Fetching the specific order of the specific user that hasnt been checked out
			specific_order = Order.objects.filter(user_id=user_id,checkout_status=False)[0:1].get()
			order_id = specific_order.id
		except:
			specific_order = None


		# if the specific user exists
		if specific_order is not None:

			try:
				#checking if the product exists in this order
				specific_order_product = OrderDetails.objects.filter(order_id =order_id , product_id=productid,is_removed=False,product_color=color,product_size=size)[0:1].get()

			except:
				specific_order_product = None

			if specific_order_product is not None:

				if specific_order_product.total_quantity >= 1:
					specific_order_product.total_quantity -= 1
					specific_order_product.remaining -= 1
					specific_order_product.total_price -= total_price
					specific_order_product.total_point -= total_point
					specific_order_product.save()
					orderdetailsserializers = OrderDetailsSerializer(specific_order_product , data=request.data)
					if orderdetailsserializers.is_valid():
						orderdetailsserializers.save()
						return JsonResponse({'success':True,'message':'The quantity has been decreased'})

			else:
				return JsonResponse({'success':False,'message':'The item does not exist'})	


		else:
			return JsonResponse({'success':False,'message':'The order does not exist'})

	else:

		try:
			#Fetching the specific order of the specific user that hasnt been checked out
			specific_order = Order.objects.filter(non_verified_user_id=non_verified_user_id,checkout_status=False)[0:1].get()
			order_id = specific_order.id
		except:
			specific_order = None


		# if the specific user exists
		if specific_order is not None:

			try:
				#checking if the product exists in this order
				specific_order_product = OrderDetails.objects.filter(order_id =order_id , product_id=productid,is_removed=False,product_color=color,product_size=size)[0:1].get()

			except:
				specific_order_product = None

			if specific_order_product is not None:

				if specific_order_product.total_quantity >= 1:
					specific_order_product.total_quantity -= 1
					specific_order_product.total_price -= total_price
					specific_order_product.total_point -= total_point
					specific_order_product.save()
					orderdetailsserializers = OrderDetailsSerializer(specific_order_product , data=request.data)
					if orderdetailsserializers.is_valid():
						orderdetailsserializers.save()
						return JsonResponse({'success':True,'message':'The quantity has been decreased'})

			else:
				return JsonResponse({'success':False,'message':'The item does not exist'})	


		else:
			return JsonResponse({'success': False,'message':'The order does not exist'})






#this removes the specific product from the cart
@api_view(['PUT',])
def delete_product(request,productid):


	color = request.data.get('color')
	size = request.data.get('size')
	#unit = request.data.get('unit')



	user_id = request.data.get('user_id')
	non_verified_user_id = request.data.get('non_verified_user_id')
	if user_id is not None:
		user_id = int(user_id)
		non_verified_user_id =0

	else:
		non_verified_user_id = int(non_verified_user_id)
		user_id = 0

	cart_count = 0  
	try:
		product_impression = ProductImpression.objects.filter(product_id=productid)[0:1].get()
	except:
		product_impression = None

	if ProductImpression is None:
		pass
	else:
		cart_count = product_impression.cart_count

	# cart = cart_count - 1
	# ProductImpression.objects.filter(product_id=productid).update(cart_count=cart)

	if non_verified_user_id == 0:

		try:
			#Fetching the specific order of the specific user that hasnt been checked out
			specific_order = Order.objects.filter(user_id=user_id,checkout_status=False)[0:1].get()
			order_id = specific_order.id
		except:
			specific_order = None


		# if the specific user exists
		if specific_order is not None:

			try:
				#checking if the product exists in this order
				specific_order_product = OrderDetails.objects.filter(order_id =order_id , product_id=productid,is_removed=False,product_color=color,product_size=size)[0:1].get()

			except:
				specific_order_product = None

			if specific_order_product is not None:

				product_quantity = specific_order_product.total_quantity
				cart = cart_count - product_quantity
				ProductImpression.objects.filter(product_id=productid).update(cart_count=cart)


				specific_order_product.is_removed = True
				specific_order_product.save()
				return JsonResponse({'success':True,'message':'The item has been removed from the cart'})

			else:
				return JsonResponse({'success': False,'message':'The item doesn not exist'})


		else:
			return JsonResponse({'success': False,'message':'The item doesn not exist'})

	else:
		try:
			#Fetching the specific order of the specific user that hasnt been checked out
			specific_order = Order.objects.filter(non_verified_user_id=non_verified_user_id,checkout_status=False)[0:1].get()
			order_id = specific_order.id
		except:
			specific_order = None


		# if the specific user exists
		if specific_order is not None:

			try:
				#checking if the product exists in this order
				specific_order_product = OrderDetails.objects.filter(order_id =order_id , product_id=productid,is_removed=False,product_color=color,product_size=size)[0:1].get()

			except:
				specific_order_product = None

			if specific_order_product is not None:

				product_quantity = specific_order_product.total_quantity
				cart = cart_count - product_quantity
				ProductImpression.objects.filter(product_id=productid).update(cart_count=cart)

				specific_order_product.is_removed = True
				specific_order_product.save()
				return JsonResponse({'success':True,'message':'The item has been removed from the cart'})


		else:
			return JsonResponse({'success':False,'message':'The item doesn not exist'})





@api_view(['POST',])
def checkout(request):

	user_id = request.data.get('user_id')
	#coupon_code = request.data.get('coupon_code')
	#print(type(coupon_code))
	non_verified_user_id = request.data.get('non_verified_user_id')
	if user_id is not None:
		user_id = int(user_id)
		non_verified_user_id =0

	else:
		non_verified_user_id = int(non_verified_user_id)
		user_id = 0

	flag = False
	product_name = ""
	product_quantity = 0
	current_quantity = 0
	current_color = ""
	current_size =""
	current_unit =""

	if non_verified_user_id == 0:

		try:
			#Fetching the specific order of the specific user that hasnt been checked out
			specific_order = Order.objects.filter(user_id=user_id,checkout_status=False)[0:1].get()

		except:
			specific_order = None

		if specific_order is not None:

			# specific_order.checkout_status = True
			# specific_order.order_status = "Unpaid"
			# specific_order.delivery_status = "To pay"
			# specific_order.ordered_date = datetime.now()
			# specific_order.save()
			order_id = specific_order.id
			order_details = OrderDetails.objects.filter(order_id =order_id,is_removed=False)
			order_ids = order_details.values_list('id',flat = True)
			order_products = order_details.values_list('product_id',flat = True)
			order_colors = order_details.values_list('product_color',flat = True)
			order_sizes = order_details.values_list('product_size',flat = True)
			#order_units = order_details.values_list('product_unit',flat = True)
			order_names = order_details.values_list('product_name',flat = True)
			order_quantity = order_details.values_list('total_quantity',flat = True)
			print(order_ids)
			for i in range(len(order_ids)):
				print("dhuklam")
				print(order_sizes[i])
				print(order_colors[i])
				#print(order_units[i])
				product = ProductSpecification.objects.filter(product_id = order_products[i],size=order_sizes[i],color=order_colors[i]).last()
				if product:
					product_quantity = product.quantity

				else:
					product_quantity = 0

				

				

				print("Ashchi")
				# print(product.title)
				# print(product.quantity)
				product_name = order_names[i]
				product_color = order_colors[i]
				product_size = order_sizes[i]
				#product_unit = order_units[i]
				if order_quantity[i] > product_quantity:
					current_quantity = product_quantity
					current_name = product_name
					current_color = product_color
					current_size = product_size
					#current_unit = product_unit
					flag = False
					break
				else:
					flag = True

			print(flag)

			if flag == True:
				print("cjeck kora possible")

				#change the coupon
				# if coupon_code == '':
				# 	specific_order.coupon_code = 
				# else:
				# 	specific_order.coupon = True



				#user can checkout
				#specific_order.coupon_code = coupon_code
				specific_order.checkout_status = True
				specific_order.order_status = "Unpaid"
				specific_order.delivery_status = "To ship"
				specific_order.ordered_date = timezone.now()
				specific_order.save()

				for i in range(len(order_products)):
					product = ProductSpecification.objects.filter(product_id = order_products[i],size=order_sizes[i],color=order_colors[i]).last()
					product_quantity = product.quantity
					product.quantity -= order_quantity[i]
					product.save()
					productserializer = ProductSpecificationSerializer(product,data=request.data)
					print("fuhfuwhuhfuewhewuhew")
					if productserializer.is_valid():
						print("ffbwybwbfywefbweyfbefb")
						productserializer.save()

						sales_count = 0  
						try:
							product_impression = ProductImpression.objects.filter(product_id=order_products[i])[0:1].get()
							print(product_impression)
						except:
							product_impression = None

						if ProductImpression is None:
							print("hochche na")
							pass
						else:
							print("hochche")
							product_impression.sales_count += order_quantity[i]
							product_impression.save()

							print(product_impression.sales_count)
					else:
						print("erroesssss")
						return JsonResponse(productserializer.errors)

				return JsonResponse({'success':True,'message':'The items have been checked out'})

			else:

				message = "You cannot checkout.We only have "+str(current_quantity)+" of item "+str(current_name)+" of color "+str(current_color)+" of size "+str(current_size)+" in our stock currently."
				return JsonResponse({'success':False,'message': message})

		else:
			return JsonResponse({'success':False,'message': 'This order does not exist'})

							
	else:

		try:
			#Fetching the specific order of the specific user that hasnt been checked out
			specific_order = Order.objects.filter(non_verified_user_id=non_verified_user_id,checkout_status=False)[0:1].get()

		except:
			specific_order = None

		if specific_order is not None:

			# specific_order.checkout_status = True
			# specific_order.order_status = "Unpaid"
			# specific_order.delivery_status = "To pay"
			# specific_order.ordered_date = datetime.now()
			# specific_order.save()
			order_id = specific_order.id
			order_details = OrderDetails.objects.filter(order_id =order_id,is_removed=False)
			order_products = order_details.values_list('product_id',flat = True)
			order_colors = order_details.values_list('product_color',flat = True)
			order_sizes = order_details.values_list('product_size',flat = True)
			#order_units = order_details.values_list('product_unit',flat = True)
			order_names = order_details.values_list('product_name',flat = True)
			order_quantity = order_details.values_list('total_quantity',flat = True)
			for i in range(len(order_products)):
				product = ProductSpecification.objects.filter(product_id = order_products[i],size=order_sizes[i],color=order_colors[i]).last()
				if product:
					product_quantity = product.quantity

				else:
					product_quantity = 0
				# print(product.title)
				# print(product.quantity)
				product_name = order_names[i]
				product_color = order_colors[i]
				product_size = order_sizes[i]
				#product_unit = order_units[i]
				if order_quantity[i] > product_quantity:
					current_quantity = product_quantity
					current_name = product_name
					current_color = product_color
					current_size = product_size
					#current_unit = product_unit
					flag = False
					break
				else:
					flag = True

			if flag == True:

				#change the coupon
				# if coupon_code == '':
				# 	specific_order.coupon_code = 
				# else:
				# 	specific_order.coupon = True



				#user can checkout
				#specific_order.coupon_code = coupon_code
				specific_order.checkout_status = True
				specific_order.order_status = "Unpaid"
				specific_order.delivery_status = "To ship"
				specific_order.ordered_date = timezone.now()
				specific_order.save()

				for i in range(len(order_products)):
					product = ProductSpecification.objects.filter(product_id = order_products[i],size=order_sizes[i],color=order_colors[i]).last()
					product_quantity = product.quantity
					product.quantity -= order_quantity[i]
					product.save()
					productserializer = ProductSpecificationSerializer(product,data=request.data)
					print("fuhfuwhuhfuewhewuhew")
					if productserializer.is_valid():
						print("ffbwybwbfywefbweyfbefb")
						productserializer.save()

						sales_count = 0  
						try:
							product_impression = ProductImpression.objects.filter(product_id=order_products[i])[0:1].get()
						except:
							product_impression = None

						if ProductImpression is None:
							pass
						else:
							product_impression.sales_count += order_quantity[i]
							product_impression.save()


					else:
						print("erroesssss")
						return JsonResponse(productserializer.errors)

				return JsonResponse({'success':True,'message':'The items have been checked out'})

			else:

				message = "You cannot checkout.We only have "+str(current_quantity)+" of item "+str(current_name)+" of color "+str(current_color)+" of size "+str(current_size)+" in our stock currently."
				return JsonResponse({'success':False,'message': message})

		else:
			return JsonResponse({'success':False,'message': 'This order does not exist'})


	




#This shows the information inside the Cart
@api_view(['POST',])
def cart_view(request):

	orders_id = -1
	checkout_id = False
	orderz= []


	arr= [
        {
            "id": orders_id,
            "date_created": "",
            "order_status": "",
            "delivery_status": "",
            "user_id": orders_id,
            "non_verified_user_id": orders_id,
            "ip_address": "",
            "checkout_status": checkout_id,
            "price_total": "0.00",
            "point_total": "0.00",
            "ordered_date": "",
            "orders": orderz
        }
    ]


	user_id = request.data.get('user_id')
	non_verified_user_id = request.data.get('non_verified_user_id')
	if user_id is not None:
		user_id = int(user_id)
		non_verified_user_id =0

	else:
		non_verified_user_id = int(non_verified_user_id)
		user_id = 0


	if non_verified_user_id == 0:


		try:
			specific_order = Order.objects.filter(user_id=user_id,checkout_status=False)
		except:
			specific_order = None


		if specific_order:


			
			orderserializer = OrderSerializer(specific_order, many = True)
			#orderdetailserializer = OrderDetailsSerializer(orderdetails , many= True)

			#orders = [orderserializer.data , orderdetailserializer.data]
			return JsonResponse({'success':True,'message':'The products in the cart are shown','data':orderserializer.data}, safe=False)

		else:
			return JsonResponse({'success':True,'message': 'There are no products in the cart','data':arr})

	

	else:

		try:
			specific_order = Order.objects.filter(non_verified_user_id=non_verified_user_id,checkout_status=False)
		except:
			specific_order = None


		if specific_order:
	
			orderserializer = OrderSerializer(specific_order, many = True)
			#orderdetailserializer = OrderDetailsSerializer(orderdetails , many= True)

			#orders = [orderserializer.data , orderdetailserializer.data]
			return JsonResponse({'success':True,'message':'The products in the cart are shown','data':orderserializer.data},safe=False)

		else:
			return JsonResponse({'success':True,'message': 'There are no products in the cart','data':arr})
		

			
@api_view(['POST',])
def cart_details(request):

	orders_id = -1
	checkout_id = False
	orderz= []
	


	arr= [
        {
            "id": orders_id,
            "date_created": "",
            "order_status": "",
            "delivery_status": "",
            "user_id": orders_id,
            "non_verified_user_id": orders_id,
            "ip_address": "",
            "checkout_status": checkout_id,
            "price_total": "0.00",
            "point_total": "0.00",
            "ordered_date": "",
            "orders": orderz,
            "specification": orderz
        }
    ]


	user_id = request.data.get('user_id')
	non_verified_user_id = request.data.get('non_verified_user_id')
	if user_id is not None:
		user_id = int(user_id)
		non_verified_user_id =0

	else:
		non_verified_user_id = int(non_verified_user_id)
		user_id = 0


	if non_verified_user_id == 0:


		try:
			specific_order = Order.objects.filter(user_id=user_id,checkout_status=False)
		except:
			specific_order = None


		if specific_order:


			
			orderserializer = OrderSerializerzz(specific_order, many = True)
			#orderdetailserializer = OrderDetailsSerializer(orderdetails , many= True)

			#orders = [orderserializer.data , orderdetailserializer.data]
			return JsonResponse({'success':True,'message':'The products in the cart are shown','data':orderserializer.data}, safe=False)

		else:
			return JsonResponse({'success':True,'message': 'There are no products in the cart','data':arr})

	

	else:

		try:
			specific_order = Order.objects.filter(non_verified_user_id=non_verified_user_id,checkout_status=False)
		except:
			specific_order = None


		if specific_order:
	
			orderserializer = OrderSerializerzz(specific_order, many = True)
			#orderdetailserializer = OrderDetailsSerializer(orderdetails , many= True)

			#orders = [orderserializer.data , orderdetailserializer.data]
			return JsonResponse({'success':True,'message':'The products in the cart are shown','data':orderserializer.data},safe=False)

		else:
			return JsonResponse({'success':True,'message': 'There are no products in the cart','data':arr})




	 	
#This shows the information of the persons all orders
@api_view(['POST',])
def all_orders(request):



	user_id = request.data.get('user_id')
	non_verified_user_id = request.data.get('non_verified_user_id')
	if user_id is not None:
		user_id = int(user_id)
		non_verified_user_id =0

	else:
		non_verified_user_id = int(non_verified_user_id)
		user_id = 0

	if non_verified_user_id == 0:

		try:
			specific_order = Order.objects.filter(user_id=user_id,checkout_status=True)
		except:
			specific_order = None


		if specific_order:


			
			orderserializer = OrderSerializer(specific_order, many = True)
			#orderdetailserializer = OrderDetailsSerializer(orderdetails , many= True)

			#orders = [orderserializer.data , orderdetailserializer.data]
			return JsonResponse({'success':True,'message':'The products in your order are shown','data':orderserializer.data}, safe=False)

		else:
			return JsonResponse({'success':False,'message': 'You have no orders'})

	

	else:

		try:
			specific_order = Order.objects.filter(non_verified_user_id=non_verified_user_id,checkout_status=True)
		except:
			specific_order = None


		if specific_order:
	
			orderserializer = OrderSerializer(specific_order, many = True)
			#orderdetailserializer = OrderDetailsSerializer(orderdetails , many= True)

			#orders = [orderserializer.data , orderdetailserializer.data]
			return JsonResponse({'success':True,'message':'The products in your orders are shown','data':orderserializer.data},safe=False)

		else:
			return JsonResponse({'success':False,'message': 'You have no orders'})



#This shows the information of the a specific
@api_view(['POST',])
def specific_order(request,order_id):



	# user_id = request.data.get('user_id')
	# non_verified_user_id = request.data.get('non_verified_user_id')
	# if user_id is not None:
	# 	user_id = int(user_id)
	# 	non_verified_user_id =0

	# else:
	# 	non_verified_user_id = int(non_verified_user_id)
	# 	user_id = 0

	# if non_verified_user_id == 0:

	try:
		specific_order = Order.objects.get(id=order_id)
		print(specific_order)
	except:
		specific_order = None


	if specific_order:


		
		orderserializer = OrderSerializer(specific_order)
		#orderdetailserializer = OrderDetailsSerializer(orderdetails , many= True)

		#orders = [orderserializer.data , orderdetailserializer.data]
		return JsonResponse({'success':True,'message':'The products in your order are shown','data':orderserializer.data}, safe=False)

	else:
		return JsonResponse({'success':False,'message': 'You have no orders'})



#This shows the information of the a specific
@api_view(['GET',])
def orders(request):



	# user_id = request.data.get('user_id')
	# non_verified_user_id = request.data.get('non_verified_user_id')
	# if user_id is not None:
	# 	user_id = int(user_id)
	# 	non_verified_user_id =0

	# else:
	# 	non_verified_user_id = int(non_verified_user_id)
	# 	user_id = 0

	# if non_verified_user_id == 0:

	try:
		specific_order = Order.objects.filter(checkout_status=True,admin_status="Confirmed")|Order.objects.filter(checkout_status=True,admin_status="Cancelled")
	except:
		specific_order = None


	if specific_order:


		
		orderserializer = OrderSerializer(specific_order, many = True)
		#orderdetailserializer = OrderDetailsSerializer(orderdetails , many= True)

		#orders = [orderserializer.data , orderdetailserializer.data]
		return JsonResponse({'success':True,'message':'The products in your order are shown','data':orderserializer.data}, safe=False)

	else:
		return JsonResponse({'success':False,'message': 'You have no orders'})

	

	# else:

	# 	try:
	# 		specific_order = Order.objects.filter(non_verified_user_id=non_verified_user_id,checkout_status=True)
	# 	except:
	# 		specific_order = None


	# 	if specific_order:
	
	# 		orderserializer = OrderSerializer(specific_order, many = True)
	# 		#orderdetailserializer = OrderDetailsSerializer(orderdetails , many= True)

	# 		#orders = [orderserializer.data , orderdetailserializer.data]
	# 		return JsonResponse({'success':True,'message':'The products in your orders are shown','data':orderserializer.data},safe=False)

	# 	else:
	# 		return JsonResponse({'success':False,'message': 'You have no orders'})



#This is for the admin panel. Shows all the orders not approved by the admin
@api_view(['GET',])
def orders_pending(request):



	# user_id = request.data.get('user_id')
	# non_verified_user_id = request.data.get('non_verified_user_id')
	# if user_id is not None:
	# 	user_id = int(user_id)
	# 	non_verified_user_id =0

	# else:
	# 	non_verified_user_id = int(non_verified_user_id)
	# 	user_id = 0

	# if non_verified_user_id == 0:

	try:
		specific_order = Order.objects.filter(checkout_status=True,admin_status="Processing")
	except:
		specific_order = None


	if specific_order:


		
		orderserializer = OrderSerializer(specific_order, many = True)
		#orderdetailserializer = OrderDetailsSerializer(orderdetails , many= True)

		#orders = [orderserializer.data , orderdetailserializer.data]
		return JsonResponse({'success':True,'message':'The products in your order are shown','data':orderserializer.data}, safe=False)

	else:
		return JsonResponse({'success':False,'message': 'You have no orders'})

	

	# else:

	# 	try:
	# 		specific_order = Order.objects.filter(non_verified_user_id=non_verified_user_id,checkout_status=True)
	# 	except:
	# 		specific_order = None


	# 	if specific_order:
	
	# 		orderserializer = OrderSerializer(specific_order, many = True)
	# 		#orderdetailserializer = OrderDetailsSerializer(orderdetails , many= True)

	# 		#orders = [orderserializer.data , orderdetailserializer.data]
	# 		return JsonResponse({'success':True,'message':'The products in your orders are shown','data':orderserializer.data},safe=False)

	# 	else:
	# 		return JsonResponse({'success':False,'message': 'You have no orders'})



#This shows the information of the user's orders that are to be paid 
@api_view(['POST',])
def orders_to_pay(request):

	user_id = request.data.get('user_id')
	non_verified_user_id = request.data.get('non_verified_user_id')
	if user_id is not None:
		user_id = int(user_id)
		non_verified_user_id =0

	else:
		non_verified_user_id = int(non_verified_user_id)
		user_id = 0

	if non_verified_user_id == 0:

		try:
			specific_order = Order.objects.filter(user_id=user_id,checkout_status=True,delivery_status="To ship",order_status="Unpaid",admin_status="Confirmed")
		except:
			specific_order = None


		if specific_order:


			
			orderserializer = OrderSerializer(specific_order, many = True)
			#orderdetailserializer = OrderDetailsSerializer(orderdetails , many= True)

			#orders = [orderserializer.data , orderdetailserializer.data]
			return JsonResponse({'success':True,'message':'The products in your order are shown','data':orderserializer.data}, safe=False)

		else:
			return JsonResponse({'success':False,'message': 'You have no orders'})

	

	else:

		try:
			specific_order = Order.objects.filter(non_verified_user_id=non_verified_user_id,checkout_status=True,delivery_status="To ship",order_status="Unpaid",admin_status="Confirmed")
		except:
			specific_order = None


		if specific_order:
	
			orderserializer = OrderSerializer(specific_order, many = True)
			#orderdetailserializer = OrderDetailsSerializer(orderdetails , many= True)

			#orders = [orderserializer.data , orderdetailserializer.data]
			return JsonResponse({'success':True,'message':'The products in your orders are shown','data':orderserializer.data},safe=False)

		else:
			return JsonResponse({'success':False,'message': 'You have no orders'})





#This shows the information of the user's orders that are to be shipped
@api_view(['POST',])
def orders_to_ship(request):

	user_id = request.data.get('user_id')
	non_verified_user_id = request.data.get('non_verified_user_id')
	if user_id is not None:
		user_id = int(user_id)
		non_verified_user_id =0

	else:
		non_verified_user_id = int(non_verified_user_id)
		user_id = 0

	if non_verified_user_id == 0:

		try:
			specific_order = Order.objects.filter(user_id=user_id,checkout_status=True,delivery_status="To ship",admin_status="Confirmed",order_status="Unpaid")|Order.objects.filter(user_id=user_id,checkout_status=True,delivery_status="To ship",admin_status="Confirmed",order_status="Paid")
		except:
			specific_order = None


		if specific_order:


			
			orderserializer = OrderSerializer(specific_order, many = True)
			#orderdetailserializer = OrderDetailsSerializer(orderdetails , many= True)

			#orders = [orderserializer.data , orderdetailserializer.data]
			return JsonResponse({'success':True,'message':'The products in your order are shown','data':orderserializer.data}, safe=False)

		else:
			return JsonResponse({'success':False,'message': 'You have no orders'})

	

	else:

		try:
			specific_order = Order.objects.filter(non_verified_user_id=non_verified_user_id,checkout_status=True,delivery_status="To ship")
		except:
			specific_order = None


		if specific_order:
	
			orderserializer = OrderSerializer(specific_order, many = True)
			#orderdetailserializer = OrderDetailsSerializer(orderdetails , many= True)

			#orders = [orderserializer.data , orderdetailserializer.data]
			return JsonResponse({'success':True,'message':'The products in your orders are shown','data':orderserializer.data},safe=False)

		else:
			return JsonResponse({'success':False,'message': 'You have no orders'})






#This shows the information of the user's orders that have already been received
@api_view(['POST',])
def orders_received(request):

	user_id = request.data.get('user_id')
	non_verified_user_id = request.data.get('non_verified_user_id')
	if user_id is not None:
		user_id = int(user_id)
		non_verified_user_id =0

	else:
		non_verified_user_id = int(non_verified_user_id)
		user_id = 0

	if non_verified_user_id == 0:

		try:
			specific_order = Order.objects.filter(user_id=user_id,checkout_status=True,delivery_status="Received",order_status="Paid",admin_status="Confirmed")
		except:
			specific_order = None


		if specific_order:


			
			orderserializer = OrderSerializer(specific_order, many = True)
			#orderdetailserializer = OrderDetailsSerializer(orderdetails , many= True)

			#orders = [orderserializer.data , orderdetailserializer.data]
			return JsonResponse({'success':True,'message':'The products in your order are shown','data':orderserializer.data}, safe=False)

		else:
			return JsonResponse({'success':False,'message': 'You have no orders'})

	

	else:

		try:
			specific_order = Order.objects.filter(non_verified_user_id=non_verified_user_id,checkout_status=True,delivery_status="Received",order_status="Paid",admin_status="Confirmed")
		except:
			specific_order = None


		if specific_order:
	
			orderserializer = OrderSerializer(specific_order, many = True)
			#orderdetailserializer = OrderDetailsSerializer(orderdetails , many= True)

			#orders = [orderserializer.data , orderdetailserializer.data]
			return JsonResponse({'success':True,'message':'The products in your orders are shown','data':orderserializer.data},safe=False)

		else:
			return JsonResponse({'success':False,'message': 'You have no orders'})



#This shows the information of the user's orders that have already been received
@api_view(['POST',])
def orders_cancelled(request):

	user_id = request.data.get('user_id')
	non_verified_user_id = request.data.get('non_verified_user_id')
	if user_id is not None:
		user_id = int(user_id)
		non_verified_user_id =0

	else:
		non_verified_user_id = int(non_verified_user_id)
		user_id = 0

	if non_verified_user_id == 0:

		try:
			specific_order = Order.objects.filter(user_id=user_id,checkout_status=True,delivery_status="Cancelled",order_status="Cancelled",admin_status="Cancelled")
		except:
			specific_order = None


		if specific_order:


			
			orderserializer = OrderSerializer(specific_order, many = True)
			#orderdetailserializer = OrderDetailsSerializer(orderdetails , many= True)

			#orders = [orderserializer.data , orderdetailserializer.data]
			return JsonResponse({'success':True,'message':'The products in your order are shown','data':orderserializer.data}, safe=False)

		else:
			return JsonResponse({'success':False,'message': 'You have no orders'})

	

	else:

		try:
			specific_order = Order.objects.filter(non_verified_user_id=non_verified_user_id,checkout_status=True,delivery_status="Cancelled",order_status="Cancelled")
		except:
			specific_order = None


		if specific_order:
	
			orderserializer = OrderSerializer(specific_order, many = True)
			#orderdetailserializer = OrderDetailsSerializer(orderdetails , many= True)

			#orders = [orderserializer.data , orderdetailserializer.data]
			return JsonResponse({'success':True,'message':'The products in your orders are shown','data':orderserializer.data},safe=False)

		else:
			return JsonResponse({'success':False,'message': 'You have no orders'})

#This shows the information of all the orders that have not been paid for 
#FOR THE PAYMENT API
@api_view(['GET',])
def orders_not_paid(request):




	try:
		specific_order = Order.objects.filter(order_status="Unpaid",checkout_status=True)
		# order_ids = specific_order.values_list('id' , flat = True)
		# orderdetails =[]
		# for i in range(len(order_ids)):
		# 	details_data = OrderDetails.objects.filter(order_id = order_ids[i],is_removed=False)
		# 	orderdetails += details_data

		if request.method == 'GET':
			orderserializer = OrderSerializer(specific_order, many = True)
			#orderdetailserializer = OrderDetailsSerializer(orderdetails , many= True)

			#orders = [orderserializer.data , orderdetailserializer.data]
			return JsonResponse(orderserializer.data , safe=False)

	except Order.DoesNotExist:
		return JsonResponse({'message': 'This order does not exist'}, status=status.HTTP_404_NOT_FOUND)

#This shows the information of all the orders that have not been delivered for 
#FOR THE DELIVERY API
@api_view(['GET',])
def orders_not_delivered(request):

	try:
		specific_order = Order.objects.filter(delivery_status="To ship",checkout_status=True)
		# order_ids = specific_order.values_list('id' , flat = True)
		# orderdetails =[]
		# for i in range(len(order_ids)):
		# 	details_data = OrderDetails.objects.filter(order_id = order_ids[i],is_removed=False)
		# 	orderdetails += details_data

		if request.method == 'GET':
			orderserializer = OrderSerializer(specific_order, many = True)
			#orderdetailserializer = OrderDetailsSerializer(orderdetails , many= True)

			#orders = [orderserializer.data , orderdetailserializer.data]
			return JsonResponse(orderserializer.data , safe=False)

	except Order.DoesNotExist:
		return JsonResponse({'message': 'This order does not exist'}, status=status.HTTP_404_NOT_FOUND)
	
#This shows the information of all the orders that have not been delivered for 
#FROM THE DELIVERY API 
@api_view(['GET',])
def order_delivery(request,order_id):

	arr={
		"delivery_charge": "45.00",
		"name": "DHL",
		"delivery_status": "delivered"  
		}


	try:
		specific_order = Order.objects.filter(id=order_id).last()
		# order_ids = specific_order.values_list('id' , flat = True)
		# orderdetails =[]
		# for i in range(len(order_ids)):
		# 	details_data = OrderDetails.objects.filter(order_id = order_ids[i],is_removed=False)
		# 	orderdetails += details_data

		if request.method == 'GET':
			orderserializer = OrderSerializer(specific_order, many = True)

			#orderdetailserializer = OrderDetailsSerializer(orderdetails , many= True)

			#orders = [orderserializer.data , orderdetailserializer.data]
			return JsonResponse({'order':orderserializer.data,'delivery_info':arr}, safe=False)

	except Order.DoesNotExist:
		return JsonResponse({'message': 'This order does not exist'}, status=status.HTTP_404_NOT_FOUND)



#This cancels the current user order
#Has to cancel within 3 days of the ordered and if delivery_status is not received
@api_view(['POST',])
def cancel_order(request):

	user_id = request.data.get('user_id')
	non_verified_user_id = request.data.get('non_verified_user_id')
	if user_id is not None:
		user_id = int(user_id)
		non_verified_user_id =0



	else:
		non_verified_user_id = int(non_verified_user_id)
		user_id = 0


	if non_verified_user_id == 0:

		try:
			specific_order =Order.objects.filter(user_id=user_id,checkout_status=True,delivery_status="To ship",order_status="Unpaid",admin_status="Processing").last()
		except:
			specific_order = None


		if specific_order is not None:


			order_date = specific_order.ordered_date
			
			cancellation_date = order_date + timedelta(days=3)
			#current_date = datetime.now()
			current_date = timezone.now()
			if current_date < cancellation_date:
				specific_order.order_status = "Cancelled"
				specific_order.delivery_status="Cancelled"
				specific_order.admin_status="Cancelled"
				specific_order.save()
				orderserializer = OrderSerializer(specific_order,request.data)
				if orderserializer.is_valid():
					orderserializer.save()
					return JsonResponse({'success':True,'message': 'This order has been cancelled'})

			else:
				return JsonResponse({'success':False,'message': 'This order cannot be cancelled now'})

		else:
			return JsonResponse({'success':False,'message': 'This order does not exist'})





	else:
		try:
			specific_order =Order.objects.filter(non_verified_user_id=non_verified_user_id,checkout_status=True,delivery_status="To ship",order_status="Unpaid",admin_status="Processing").last()
		except:
			specific_order = None


		if specific_order is not None:


			order_date = specific_order.ordered_date
			
			cancellation_date = order_date + timedelta(days=3)
			#current_date = datetime.now()
			current_date = timezone.now()
			if current_date < cancellation_date:
				specific_order.order_status = "Cancelled"
				specific_order.delivery_status="Cancelled"
				specific_order.admin_status="Cancelled"
				specific_order.save()
				orderserializer = OrderSerializer(specific_order,request.data)
				if orderserializer.is_valid():
					orderserializer.save()
					return JsonResponse({'success':True,'message': 'This order has been cancelled'})

			else:
				return JsonResponse({'success':False,'message': 'This order cannot be cancelled now'})

		else:
			return JsonResponse({'success':False,'message': 'This order does not exist'})
		

#This cancels a specific order
#Has to cancel within 3 days of the ordered and if delivery_status is to ship and order_status is unpaid
@api_view(['POST',])
def cancel_specific_order(request,order_id):



	try:
		specific_order =Order.objects.get(id=order_id)
	except:
		specific_order = None


	if specific_order is not None:

		if (specific_order.delivery_status == "To ship") and (specific_order.order_status == "Unpaid") and (specific_order.admin_status == "Processing"):


			order_date = specific_order.ordered_date
			
			cancellation_date = order_date + timedelta(days=3)
			#current_date = datetime.now()
			current_date = timezone.now()
			if current_date < cancellation_date:
				specific_order.order_status = "Cancelled"
				specific_order.delivery_status="Cancelled"
				specific_order.admin_status="Cancelled"
				specific_order.save()
				orderserializer = OrderSerializer(specific_order,request.data)
				if orderserializer.is_valid():
					orderserializer.save()
					return JsonResponse({'success':True,'message': 'This order has been cancelled'})

			else:
				return JsonResponse({'success':False,'message': 'This order cannot be cancelled now'})

		else:
			return JsonResponse({'success':False,'message': 'This order has already been paid and shipped for or has been cancelled'})


	else:
		return JsonResponse({'success':False,'message': 'This order does not exist'})







@api_view(['POST',])
def cancelorder(request,order_id):



	try:
		specific_order =Order.objects.get(id=order_id)
	except:
		specific_order = None


	if specific_order is not None:

		if specific_order.admin_status == "Processing":

			specific_order.order_status = "Cancelled"
			specific_order.delivery_status = "Cancelled"
			specific_order.admin_status = "Cancelled"
			specific_order.save()
			orderserializer = OrderSerializer(specific_order,request.data)
			if orderserializer.is_valid():
				orderserializer.save()
				return JsonResponse({'success':True,'message': 'This order has been cancelled'})

			else:
				return JsonResponse({'success':False,'message': 'This order cannot be cancelled now'})

		else:
			return JsonResponse({'success':False,'message': 'This order has already been cofirmed by the admin'})


	else:
		return JsonResponse({'success':False,'message': 'This order does not exist'})














#if items are inside the cart and hasnt been checked out the order will be cancelled within 2 days
@api_view(['POST',])
def cancel_cart(request):

	user_id = request.data.get('user_id')
	non_verified_user_id = request.data.get('non_verified_user_id')
	if user_id is not None:
		user_id = int(user_id)
		non_verified_user_id =0



	else:
		non_verified_user_id = int(non_verified_user_id)
		user_id = 0

	if non_verified_user_id == 0:
		

		try:
			specific_order = Order.objects.filter(user_id=user_id,checkout_status=False)[0:1].get()
			
		except:
			specific_order = None

		if specific_order is not None:

			order_date = specific_order.date_created
			cancellation_date = order_date + timedelta(days=2)
			current_date = timezone.now()
			if current_date > cancellation_date:
				specific_order.checkout_status = True
				specific_order.order_status = "Cancelled"
				specific_order.delivery_status = "Cancelled"
				specific_order.save()
				orderserializer = OrderSerializer(specific_order,request.data)
				if orderserializer.is_valid():
					orderserializer.save()
					return JsonResponse({'success':True,'message': 'This cart has been cancelled due to not been checked out within two days'})

			else:
				return JsonResponse({'success':False,'message': 'This cart still does not have to be cancelled'})

		else:
			return JsonResponse({'success':False,'message': 'This cart does not exist'})



	else:
		try:
			specific_order = Order.objects.filter(non_verified_user_id=non_verified_user_id,checkout_status=False)[0:1].get()
			
		except:
			specific_order = None

		if specific_order is not None:

			order_date = specific_order.date_created
			cancellation_date = order_date + timedelta(days=2)
			current_date = timezone.now()
			if current_date > cancellation_date:
				specific_order.checkout_status = True
				specific_order.order_status = "Cancelled"
				specific_order.delivery_status = "Cancelled"
				specific_order.save()
				orderserializer = OrderSerializer(specific_order,request.data)
				if orderserializer.is_valid():
					orderserializer.save()
					return JsonResponse({'success':True,'message': 'This cart has been cancelled due to not been checked out within two days'})

			else:
				return JsonResponse({'success':False,'message': 'This cart still does not have to be cancelled'})

		else:
			return JsonResponse({'success':False,'message': 'This cart does not exist'})


# Admin Approval
@api_view(['GET',])
def admin_approval(request,order_id):


		

	try:
		specific_order = Order.objects.get(id=order_id)
		
	except:
		specific_order = None

	if specific_order is not None:


		specific_order.admin_status = "Confirmed"

		orderserializer = OrderSerializer(specific_order,request.data)
		if orderserializer.is_valid():
			orderserializer.save()
			return JsonResponse({'success':True,'message': 'This order has been approved'})

		else:
			return JsonResponse({'success':False,'message': 'This order does not exist'})

	else:
		return JsonResponse({'success':False,'message': 'This order does not exist'})




# Admin Approval
@api_view(['GET',])
def admin_cancellation(request,order_id):


		

	try:
		specific_order = Order.objects.get(id=order_id)
		
	except:
		specific_order = None

	if specific_order is not None:


		specific_order.admin_status = "Cancelled"

		orderserializer = OrderSerializer(specific_order,request.data)
		if orderserializer.is_valid():
			orderserializer.save()
			return JsonResponse({'success':True,'message': 'This order has been cancelled'})

		else:
			return JsonResponse({'success':False,'message': 'This order does not exist'})

	else:
		return JsonResponse({'success':False,'message': 'This order does not exist'})






'''
@api_view(['POST',])
def show_address(request,userid):

	try:
		user_address = Userz.objects.filter(id = userid)[0:1].get()
		address = user_address.address

	except Address.DoesNotExist:
		user_address = None


	if user_address is not None:

'''
#this creates the address and the billing address for the user
@api_view(['POST',])
def create_address(request):

	user_id = request.data.get('user_id')
	non_verified_user_id = request.data.get('non_verified_user_id')
	if user_id is not None:
		user_id = int(user_id)
		non_verified_user_id =0



	else:
		non_verified_user_id = int(non_verified_user_id)
		user_id = 0

	if non_verified_user_id == 0:

		# address_serializer = UserzSerializer(data=request.data)
		# if address_serializer.is_valid():
		# 	address_serializer.save()

		#Create a billing address for that user
		billing_address = BillingAddress(user_id = user_id,address=request.data.get('address'))
		billing_address.save()
		billing_address_serializer = BillingAddressSerializer(billing_address,data=request.data)
		if billing_address_serializer.is_valid():
			billing_address_serializer.save()

		#addresses = [address_serializer.data,billing_address_serializer.data]
		return JsonResponse(address_serializer.data,safe=False,status=status.HTTP_201_CREATED)

	else:

		# address_serializer = UserzSerializer(data=request.data)
		# if address_serializer.is_valid():
		# 	address_serializer.save()

		#Create a billing address for that user
		billing_address = BillingAddress(non_verified_user_id = non_verified_user_id,address=request.data.get('address'))
		billing_address.save()
		billing_address_serializer = BillingAddressSerializer(billing_address,data=request.data)
		if billing_address_serializer.is_valid():
			billing_address_serializer.save()

		#addresses = [address_serializer.data,billing_address_serializer.data]
		return JsonResponse(billing_address_serializer.data,safe=False,status=status.HTTP_201_CREATED)


#This shows the address of the user in the form
@api_view(['POST',])
def show_address(request):

	num =-1

	arr = {
        "id": num,
        "user_id": num,
        "date_created": "",
        "date_updated": "",
        "non_verified_user_id": num,
        "ip_address": "",
        "phone_number": "",
        "address": "",
        "area": "",
        "location": ""
    
    }

	user_id = request.data.get('user_id')
	non_verified_user_id = request.data.get('non_verified_user_id')
	if user_id is not None:
		user_id = int(user_id)
		non_verified_user_id =0



	else:
		non_verified_user_id = int(non_verified_user_id)
		user_id = 0
         


	if non_verified_user_id == 0:

		try:
			address = BillingAddress.objects.filter(user_id=user_id).last()
			
		except:
			address = None


		if address:	
			billing_address_serializers = BillingAddressSerializer(address,many=False)
			return JsonResponse({'success':True,'data':billing_address_serializers.data},safe=False)

		else:
			#Fetching the exisitng user's address
			try:

				existing_address = Profile.objects.filter(user_id=user_id).last()
			except:
				existing_address = None

			
			if existing_address:
				
				
				#billing_address = existing_address.address
				# phone_number = existing_address.phone_number
				# city = existing_address.city
				# district = existing_address.district
				# road_number = existing_address.road_number
				# building_number = existing_address.building_number
				# apartment_number = existing_address.apartment_numbe
				if existing_address.address:
					print("1")
					address = existing_address.address
				else:
					address = ""
				if existing_address.phone_number:
					print("2")
					phone_number = existing_address.phone_number
				else:
					phone_number = ""

				if existing_address.name:
					print("3")
					name = existing_address.name
				else:
					name = ""
				if existing_address.area:
					print("4")
					area = existing_address.area
				else:
					area= ""
				if existing_address.location:
					print("5")
					location = existing_address.location

				else:
					location = ""
				#create a billing address 
				billing_address_obj = BillingAddress.objects.create(user_id=user_id,phone_number=phone_number,address=address,name=name,area=area,location=location)
				billing_address_obj.save()
				billing_serializer = BillingAddressSerializer(billing_address_obj,data=request.data)
				if billing_serializer.is_valid():
					billing_serializer.save()
					return JsonResponse({'success':True,'data':billing_serializer.data})
				else:
					return JsonResponse(billing_serializer.errors)


			else:
				

				
				# billing_address_obj = BillingAddress.objects.create(user_id=user_id)
				# billing_address_obj.save()
				# billing_serializer = BillingAddressSerializer(billing_address_obj,data=request.data)
				# if billing_serializer.is_valid():
				# 	billing_serializer.save()
				return JsonResponse({'success':False,'data':[arr]})
				# else:
				# 	return JsonResponse(billing_serializer.errors)

	else:
		print("Coming HERE")
		try:

			address = BillingAddress.objects.filter(non_verified_user_id=non_verified_user_id).last()
			#print(address)

		except:
			address = None

			

		if address is None:
			#print("Yessssss")
			return JsonResponse({'success':False,'data':arr})
			
		else:
			#print("Coming here")
			billing_address_serializer = BillingAddressSerializer(address)
			return JsonResponse({'success':True,'data':billing_address_serializer.data})
				

	



#this edits the billing address of a verified user and creates and edits the address of a non verified user
@api_view(['POST',])
def edit_address(request):

	user_id = request.data.get('user_id')
	non_verified_user_id = request.data.get('non_verified_user_id')
	if user_id is not None:
		user_id = int(user_id)
		non_verified_user_id =0



	else:
		non_verified_user_id = int(non_verified_user_id)
		user_id = 0

	if non_verified_user_id == 0:

		try:
			address = BillingAddress.objects.filter(user_id=user_id).last()
		except:
			address = None

		if address:

			
			billing_address_serializer = BillingAddressSerializer(address,data = request.data)
			if billing_address_serializer.is_valid():
				billing_address_serializer.save()
				return JsonResponse({'success':True,'data':billing_address_serializer.data},safe=False)

		else:

			#create a new billing address
			billing_address_serializer = BillingAddressSerializer(data=request.data)
			if billing_address_serializer.is_valid():
				billing_address_serializer.save()
				return JsonResponse({'success':True,'data':billing_address_serializer.data},safe=False)

		# else:
		# 	return JsonResponse({'success':False,'data':{}},safe=False)


		
	else:
		try:
			address = BillingAddress.objects.filter(non_verified_user_id=non_verified_user_id).last()
			if address is not None:

				billing_address_serializer = BillingAddressSerializer(address,data = request.data)
				if billing_address_serializer.is_valid():
					billing_address_serializer.save()
					return JsonResponse({'success':True,'data':billing_address_serializer.data})

			else:
				billing_address_serializer = BillingAddressSerializer(data = request.data)
				if billing_address_serializer.is_valid():
					billing_address_serializer.save()
					return JsonResponse({'success':True,'data':billing_address_serializer.data},safe=False)


				

		except BillingAddress.DoesNotExist:
			return JsonResponse({'message': 'This address does not exist'}, status=status.HTTP_404_NOT_FOUND)





@api_view(['POST',])
def check_coupon(request):

	current_date = timezone.now().date()
	coupon_percent = 0
	flag = False
	coupon_code = request.data.get('coupon_code')
	user_id = request.data.get('user_id')
	non_verified_user_id = request.data.get('non_verified_user_id')
	if user_id is not None:
		user_id = int(user_id)
		non_verified_user_id =0

	else:
		non_verified_user_id = int(non_verified_user_id)
		user_id = 0

	if non_verified_user_id == 0:
	
		try:
			#Fetching the specific order of the specific user that hasnt been checked out
			specific_order = Order.objects.filter(user_id=user_id,checkout_status=False)[0:1].get()
			print("HOITESE NAAAAAAAAAAAAA")
			print(specific_order)

		except:
			specific_order = None

		if specific_order is not None:
			print("hfeufhfgfwgyrgfrygr")
			specific_order.coupon_code = coupon_code
			specific_order.save()
			orderserializer = OrderSerializer(specific_order,request.data)
			if orderserializer.is_valid():
				orderserializer.save()

	else:
		try:

			#Fetching the specific order of the specific user that hasnt been checked out
			specific_order = Order.objects.filter(non_verified_user_id=non_verified_user_id,checkout_status=False)[0:1].get()
			print("HOITESE NAAAAAAAAAAAAA")
			print(specific_order)

		except:
			specific_order = None

		if specific_order is not None:
			print("hfeufhfgfwgyrgfrygr")
			specific_order.coupon_code = coupon_code
			specific_order.save()
			orderserializer = OrderSerializer(specific_order,request.data)
			if orderserializer.is_valid():
				orderserializer.save()



	coupons = Cupons.objects.all()
	coupon_codes = list(coupons.values_list('cupon_code',flat=True))
	coupon_amounts = list(coupons.values_list('amount',flat=True))
	coupon_start = list(coupons.values_list('start_from',flat=True))
	coupon_end = list(coupons.values_list('valid_to',flat=True))
	coupon_validity = list(coupons.values_list('is_active',flat=True))

	for i in range(len(coupon_codes)):
		if (coupon_codes[i]==coupon_code and current_date>=coupon_start[i] and current_date <= coupon_end[i] and coupon_validity[i]==True):

			coupon_percent = coupon_amounts[i]
			flag = True
			break
		else:
			flag = False

	if flag == True:
		return JsonResponse({'success':True,'message': 'Promo code applied'})

	else:
		return JsonResponse({'success':False,'message': 'Promo code is not applied'})




#This is for the Delivery API and the payment site 
@api_view(['POST',])
def send_info(request,order_id):


	data = request.data 


	try:

		specific_order = Order.objects.get(id = order_id)


	except: 


		specific_order = None 


	if specific_order:

		if specific_order.user_id == -1:

			non_verified_user_id = specific_order.non_verified_user_id
			user_id = -1

		else:
			user_id = specific_order.user_id
			non_verified_user_id = -1 




		if non_verified_user_id == -1:


			try:
				address = BillingAddress.objects.filter(user_id=user_id).last()
			except:
				address = None

			if address:

				address_serializer = BillingAddressSerializer(address,many=False)

				address_data = address_serializer.data

			else:

				address_data = {}

		else:


			try:
				address = BillingAddress.objects.filter(non_verified_user_id=non_verified_user_id).last()
			except:
				address = None

			if address:

				address_serializer = BillingAddressSerializer(address,many=False)

				address_data = address_serializer.data

			else:

				address_data = {}




		order_serializer = OrderSerializer(specific_order,many=False)

		order_info = order_serializer.data

	else:

		order_info = {}
		address_data = {}


	try:

		company_info = CompanyInfo.objects.all()[0:1].get()


	except:

		company_info = None


	if company_info:

		company_name = company_info.name

	else:

		company_name = ""



	return JsonResponse({'success':True,'message':'Data is shown below','company_name':company_name,'order_info':order_info,'billing_address':address_data,'other_info':data })





































        

























		





			




	

			
            
            

            
		    


















	

