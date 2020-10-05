from django.shortcuts import render
from django.http import HttpResponse
from django.http.response import JsonResponse
from rest_framework.parsers import JSONParser 
from rest_framework import status
import datetime
from Intense.models import Category,Sub_Category,Sub_Sub_Category,Product

from .serializers import CategorySerializer,CategorySerializerz,Sub_CategorySerializer,Sub_Sub_CategorySerializer,CatSerializer,SubCatSerializer,SubSubCatSerializer
from Product_details.serializers import ProductImpressionSerializer
from rest_framework.decorators import api_view 
from django.views.decorators.csrf import csrf_exempt
from datetime import datetime
from datetime import timedelta  
from django.utils import timezone
from Product.serializers import ProductSerializer,SearchSerializer

@api_view(['POST',])
def insert_category(request):

	category = request.data.get('category')
	sub_category = request.data.get('sub_category')
	sub_sub_category = request.data.get('sub_sub_category')
	category_id = 0
	sub_category_id = 0
	sub_sub_category_id = 0

	
	existing = Category.objects.order_by('timestamp')
	existing_categories = list(existing.values_list('title',flat=True).distinct())
	existing_ids = list(existing.values_list('id',flat=True).distinct())
	# print(existing_categories)
	# print(existing_ids)

	# existing_sub = Sub_Category.objects.all()
	# existing_sub_categories = list(existing.values_list('title',flat=True).distinct())

	if category != "None":	

		if category not in existing_categories:
			#print("new catagory")

			#print("New Category")

			#Create a new category

			new_category = Category.objects.create(title=category)
			new_category.save()
			category_id = new_category.id
			categoryserializer = CategorySerializer(new_category , data=request.data)
			if categoryserializer.is_valid():
				categoryserializer.save()
			else:
				return JsonResponse(categoryserializer.errors)

			#print(category_id)

			if sub_category != "None":
				#print("New sub category for that new category")

				#Create a sub category for that category

				new_sub_category = Sub_Category.objects.create(title=sub_category,category_id=category_id)
				new_sub_category.save()
				sub_category_id = new_sub_category.id
				sub_categoryserializer = Sub_CategorySerializer(new_sub_category , data=request.data)
				if sub_categoryserializer.is_valid():
					sub_categoryserializer.save()
				else:
					return JsonResponse(sub_categoryserializer.errors)

				#print(sub_category_id)



				if sub_sub_category != "None":

					#print("new sub sub for that new category")

					#Create a sub sub category for that sub category

					new_sub_sub_category = Sub_Sub_Category.objects.create(title=sub_sub_category,sub_category_id=sub_category_id)
					new_sub_sub_category.save()
					sub_sub_category_id = new_sub_sub_category.id
					sub_sub_categoryserializer = Sub_Sub_CategorySerializer(new_sub_category , data=request.data)
					if sub_sub_categoryserializer.is_valid():
						sub_sub_categoryserializer.save()
					else:
						return JsonResponse(sub_sub_categoryserializer.errors)


					#print(sub_sub_category_id)

				else:
					sub_sub_category_id = 0

			else:
				sub_category_id = 0

	# data={'category':category_id,'sub_category':sub_category_id,'sub_sub_category':sub_sub_category_id}
	# return JsonResponse(data)

		else:
			#print("same category")
			#Fetch which category
			# print(existing_ids)
			for i in range(len(existing_ids)):
				if category == existing_categories[i]:
					category_id = existing_ids[i]
					break
					#print(category_id)

			existing_subs = Sub_Category.objects.filter(category_id=category_id).order_by('timestamp')
			existing_sub_categories = list(existing_subs.values_list('title',flat=True).distinct())
			existing_sub_ids = list(existing_subs.values_list('id',flat=True).distinct())
			#existing_sub_idss = list(existing_subs.values_list('id','title',flat=True).distinct())

			if sub_category != "None":

				if sub_category not in existing_sub_categories:
					#print("new sub for same category")

					#Create a  new sub category for that category

					new_sub_category = Sub_Category.objects.create(title=sub_category,category_id=category_id)
					new_sub_category.save()
					sub_category_id = new_sub_category.id
					sub_categoryserializer = Sub_CategorySerializer(new_sub_category , data=request.data)
					if sub_categoryserializer.is_valid():
						sub_categoryserializer.save()
					else:
						return JsonResponse(sub_categoryserializer.errors)



					if sub_sub_category != "None":

						#print("create a sub sub for the new sub category")

						#Create a sub sub category for that sub category

						new_sub_sub_category = Sub_Sub_Category.objects.create(title=sub_sub_category,sub_category_id=sub_category_id)
						new_sub_sub_category.save()
						sub_sub_category_id = new_sub_sub_category.id
						sub_sub_categoryserializer = Sub_Sub_CategorySerializer(new_sub_category , data=request.data)
						if sub_sub_categoryserializer.is_valid():
							sub_sub_categoryserializer.save()
						else:
							return JsonResponse(sub_sub_categoryserializer.errors)


					else:
						sub_sub_category_id = 0


				else:

					#print("same sub category for same category")


					#Fetch which sub category
					#print(existing_sub_idss)

					
					for i in range(len(existing_sub_ids)):

						#print(existing_sub_ids)

						#print(existing_sub_categories)


						if sub_category == existing_sub_categories[i]:
							# print(existing_sub_categories[i])
							# print(existing_sub_ids[i])
							sub_category_id = existing_sub_ids[i]
							#print(sub_category_id)
							break

							#print(sub_category_id)
							

					existing_sub_subs = Sub_Sub_Category.objects.filter(sub_category_id=sub_category_id).order_by('timestamp')
					existing_sub_sub_categories = list(existing_sub_subs.values_list('title',flat=True))
					existing_sub_sub_ids = list(existing_sub_subs.values_list('id',flat=True))

					if sub_sub_category != "None":

						if sub_sub_category not in existing_sub_sub_categories:

							#print("new sub sub category for the same sub ")
							

							#Create a new sub_sub_category

							new_sub_sub_category = Sub_Sub_Category.objects.create(title=sub_sub_category,sub_category_id=sub_category_id)
							new_sub_sub_category.save()
							sub_sub_category_id = new_sub_sub_category.id
							sub_sub_categoryserializer = Sub_Sub_CategorySerializer(new_sub_sub_category , data=request.data)
							if sub_sub_categoryserializer.is_valid():
								sub_sub_categoryserializer.save()

							#print(sub_sub_category_id)


						else:
							#print("3 tai same")

							#Fetch the sub_sub_category_id
							for i in range(len(existing_sub_sub_ids)):
								if sub_sub_category == existing_sub_sub_categories[i]:
									sub_sub_category_id = existing_sub_sub_ids[i]
									break

					else:
						sub_sub_category_id = 0

			else:

				sub_category_id = 0

	else:

		category = 0


	data={'category':category_id,'sub_category':sub_category_id,'sub_sub_category':sub_sub_category_id}
	return JsonResponse(data)






@api_view(['GET',])
def products_section(request,ids,level):


	#ids = request.data.get('id')
	# level = request.data.get('level')
	# sub_sub_category_id = request.data.get('sub_sub_category')

	if level == "First":


		try:

			products = Product.objects.filter(category_id=ids)

		except:

			products = None

		if products:

			products_serializers = SearchSerializer(products,many=True)
			response_data = products_serializers.data
			product_ids = []
			# for i in range
			#print(products_serializers.data[0]['id'])
			for i in range(len(products_serializers.data)):
				product_id = products_serializers.data[i]['id']
				product_ids.append(product_id)


			
			queryset = Product.objects.filter(pk__in = product_ids)
			product_brands = list(queryset.values_list('brand',flat=True).distinct())


			if 'brand' in request.GET:
				my_brand = request.GET['brand']
				queryset = queryset.filter(brand=my_brand)
			else:
				my_brand =''

			# new_querys = queryset.filter(brand=my_brand)

			product_serializers = SearchSerializer(queryset , many = True)
			response_data = product_serializers.data


			rating_data = []
			if 'ratings' in request.GET:
				print("rating ey dhukse")
				my_ratings = request.GET['ratings']
				rating_list = [1,2,3,4,5]
				for pro in response_data:
					for key, value in pro.items(): 
						if(key=='ratings' and value):
							if(value['average_ratings']>= float(my_ratings)):
								rating_data.append(pro)

				response_data = rating_data


        # if (rating_data):
        #     print("rating ase")

        #     response_data = rating_data


			price_data = []

			if 'max_price' or 'min_price' in request.GET:
				print("price ey dhukse")
				if 'max_price' in request.GET:
					max_price = request.GET['max_price']

				else:
					max_price = 100000000 

				if 'min_price' in request.GET:
					min_price = request.GET['min_price']

				else:
					min_price = 0


				for pro in response_data:
					for key, value in pro.items(): 
						if(key=='new_price' and value):
							print(min_price)
							if((float(value) >= float(min_price)) and (float(value) <= float(max_price))):
								price_data.append(pro)

				response_data = price_data


			return JsonResponse({'success':True ,'data':response_data,'brands':product_brands}, safe=False)
		else:
			return JsonResponse({'success':False ,'data':[]})



	elif level == "Second":

		try:

			products = Product.objects.filter(sub_category_id=ids)

		except:

			products = None

		if products:

			products_serializers = SearchSerializer(products,many=True)
			response_data = products_serializers.data
			product_ids = []
			# for i in range
			#print(products_serializers.data[0]['id'])
			for i in range(len(products_serializers.data)):
				product_id = products_serializers.data[i]['id']
				product_ids.append(product_id)


			
			queryset = Product.objects.filter(pk__in = product_ids)
			product_brands = list(queryset.values_list('brand',flat=True).distinct())


			if 'brand' in request.GET:
				my_brand = request.GET['brand']
				queryset = queryset.filter(brand=my_brand)
			else:
				my_brand =''

			

			product_serializers = SearchSerializer(queryset , many = True)
			response_data = product_serializers.data


			rating_data = []
			if 'ratings' in request.GET:
				print("rating ey dhukse")
				my_ratings = request.GET['ratings']
				rating_list = [1,2,3,4,5]
				for pro in response_data:
					for key, value in pro.items(): 
						if(key=='ratings' and value):
							if(value['average_ratings']>= float(my_ratings)):
								rating_data.append(pro)

				response_data = rating_data


        # if (rating_data):
        #     print("rating ase")

        #     response_data = rating_data


			price_data = []

			if 'max_price' or 'min_price' in request.GET:
				print("price ey dhukse")
				if 'max_price' in request.GET:
					max_price = request.GET['max_price']

				else:
					max_price = 100000000 

				if 'min_price' in request.GET:
					min_price = request.GET['min_price']

				else:
					min_price = 0


				for pro in response_data:
					for key, value in pro.items(): 
						if(key=='new_price' and value):
							print(min_price)
							if((float(value) >= float(min_price)) and (float(value) <= float(max_price))):
								price_data.append(pro)

				response_data = price_data


			return JsonResponse({'success':True ,'data':response_data,'brands':product_brands}, safe=False)
		else:
			return JsonResponse({'success':False ,'data':[]})




	elif level == "Third":

		try:

			products = Product.objects.filter(sub_sub_category_id=ids)

		except:

			products = None

		if products:

			products_serializers = SearchSerializer(products,many=True)
			response_data = products_serializers.data
			print("first")
			print(response_data)
			product_ids = []
			# for i in range
			#print(products_serializers.data[0]['id'])
			for i in range(len(products_serializers.data)):
				product_id = products_serializers.data[i]['id']
				product_ids.append(product_id)



			
			queryset = Product.objects.filter(pk__in = product_ids)
			print(queryset)
			product_brands = list(queryset.values_list('brand',flat=True).distinct())



			if 'brand' in request.GET:
				print("brand ase")
				my_brand = request.GET['brand']
				queryset = queryset.filter(brand=my_brand)
			else:
				print("brand nai")
				my_brand =''

			


			product_serializers = SearchSerializer(queryset , many = True)
			response_data = product_serializers.data
			print("third")
			print(response_data)


			rating_data = []
			if 'ratings' in request.GET:
				print("rating ey dhukse")
				my_ratings = request.GET['ratings']
				rating_list = [1,2,3,4,5]
				for pro in response_data:
					for key, value in pro.items(): 
						if(key=='ratings' and value):
							if(value['average_ratings']>= float(my_ratings)):
								rating_data.append(pro)

				response_data = rating_data


        # if (rating_data):
        #     print("rating ase")

        #     response_data = rating_data


			price_data = []

			if 'max_price' or 'min_price' in request.GET:
				print("price ey dhukse")
				if 'max_price' in request.GET:
					max_price = request.GET['max_price']

				else:
					max_price = 100000000 

				if 'min_price' in request.GET:
					min_price = request.GET['min_price']

				else:
					min_price = 0


				for pro in response_data:
					for key, value in pro.items(): 
						if(key=='new_price' and value):
							print(min_price)
							if((float(value) >= float(min_price)) and (float(value) <= float(max_price))):
								price_data.append(pro)

				response_data = price_data


			return JsonResponse({'success':True ,'data':response_data,'brands':product_brands}, safe=False)
		else:
			return JsonResponse({'success':False ,'data':[]})






@api_view(['GET',])
def allcategories(request):


	#category_id = request.data.get('category')
	# sub_category_id = request.data.get('sub_category')
	# sub_sub_category_id = request.data.get('sub_sub_category')


	try:


		categories = Category.objects.all()

	except:

		categories = None 

		


	if categories:

		products_serializers = CategorySerializer(categories,many=True)
		return JsonResponse(products_serializers.data,safe=False)

	else:

		return JsonResponse([],safe=False)





















# 

			

				




		
# 	else:
# 		print("It isnt working")

# 	return JsonResponse({'success':True})


@api_view(['GET',])
def categories(request):


	try:


		categories = Category.objects.all()

	except:

		categories = None 


	if categories:

		cats = list(categories.values_list('title',flat=True).distinct())

		#products_serializers = CatSerializer(categories,many=True)
		return JsonResponse(cats,safe=False)

	else:
		return JsonResponse([])




@api_view(['POST',])
def sub_categories(request):


	category = request.data.get('name')


	try:


		categories = Category.objects.filter(title=category)

	except:

		categories = None 


	if categories:

		cats = list(categories.values_list('id',flat=True).distinct())

		try:
		
			subcats = Sub_Category.objects.filter(category_id__in = cats)

		except:

			subcats = None



		subs = list(subcats.values_list('title',flat=True).distinct())

		return JsonResponse(subs,safe=False)





	else:
		return JsonResponse([],safe=False)




@api_view(['POST',])
def sub_sub_categories(request):


	sub_category = request.data.get('name')


	try:


		sub_categories = Sub_Category.objects.filter(title=sub_category)

	except:

		sub_categories = None 


	if sub_categories:

		cats = list(sub_categories.values_list('id',flat=True).distinct())

		try:
		
			subcats = Sub_Sub_Category.objects.filter(sub_category_id__in = cats)

		except:

			subcats = None



		subs = list(subcats.values_list('title',flat=True).distinct())

		return JsonResponse(subs,safe=False)





	else:
		return JsonResponse([],safe=False)




