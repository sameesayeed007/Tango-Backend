from django.shortcuts import render
from django.http import HttpResponse
from django.http.response import JsonResponse
from rest_framework.parsers import JSONParser 
from rest_framework import status
import datetime
from Intense.models import Category,Sub_Category,Sub_Sub_Category,Product

from .serializers import CategorySerializer,CategorySerializerz,Sub_CategorySerializer,Sub_Sub_CategorySerializer
from Product_details.serializers import ProductImpressionSerializer
from rest_framework.decorators import api_view 
from django.views.decorators.csrf import csrf_exempt
from datetime import datetime
from datetime import timedelta  
from django.utils import timezone
from Product.serializers import ProductSerializer

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






@api_view(['POST',])
def products_section(request):


	ids = request.data.get('id')
	level = request.data.get('level')
	# sub_sub_category_id = request.data.get('sub_sub_category')

	if level == "First":

		try:

			products = Product.objects.filter(category_id=ids)

		except:

			products = None

		if products:

			products_serializers = ProductSerializer(products,many=True)
			return JsonResponse({'success':True ,'data':products_serializers.data}, safe=False)
		else:
			return JsonResponse({'success':False ,'data':[]})

	elif level == "Second":

		try:

			products = Product.objects.filter(sub_category_id=ids)

		except:

			products = None

		if products:

			products_serializers = ProductSerializer(products,many=True)
			return JsonResponse({'success':True ,'data':products_serializers.data}, safe=False)
		else:
			return JsonResponse({'success':False ,'data':[]})


	elif level == "Third":

		try:

			products = Product.objects.filter(sub_sub_category_id=ids)

		except:

			products = None

		if products:

			products_serializers = ProductSerializer(products,many=True)
			return JsonResponse({'success':True ,'data':products_serializers.data}, safe=False)
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

		products_serializers = CategorySerializerz(categories,many=True)
		return JsonResponse({'success':True,'data':products_serializers.data},safe=False)



@api_view(['GET',])
def sub_categories(request):


	try:


		categories = Sub_Category.objects.all()

	except:

		categories = None 


	if categories:

		products_serializers = Sub_CategorySerializer(categories,many=True)
		return JsonResponse({'success':True,'data':products_serializers.data},safe=False)



@api_view(['GET',])
def sub_sub_categories(request,sub_category_id):


	try:


		categories = Sub_Sub_Category.objects.filter(sub_category_id = sub_category_id)

	except:

		categories = None 


	if categories:

		products_serializers = Sub_Sub_CategorySerializer(categories,many=True)
		return JsonResponse({'success':True,'data':products_serializers.data},safe=False)