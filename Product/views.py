import json
import requests
from rest_framework.decorators import api_view
from django.contrib import auth
from django.core.cache import cache
from django.conf import settings
from django.core.cache.backends.base import DEFAULT_TIMEOUT
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.views.decorators.vary import vary_on_cookie
from django.utils.translation import ugettext_lazy as _

from rest_framework.generics import (
    ListAPIView,
    RetrieveAPIView,
    CreateAPIView,
    DestroyAPIView,
)
from rest_framework import permissions, status
from rest_framework.exceptions import PermissionDenied, NotAcceptable, ValidationError
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
#from rest_framework import filters
from rest_framework import viewsets
from Product_details.serializers import ProductDetailSerializer


from Intense.models import Category, Product, GroupProduct , Variation
# from user_profile.models import User

from .serializers import (
		CategorySerializer, 
		ProductSerializer,
        VariationSerializer,
        GroupProductSerialyzer,
        CreateProductSerializer,
        ProductImageSerializer,
        CommentSerializer,
        CommentReplySerializer,
        ReviewsSerializer,
        ProductReviewSerializer,
        ProductCodeSerializer,
        ScannerProductSerializer,
        AllGroupProductSerialyzer,
        SearchSerializer,

		)


from .decorators import time_calculator
from Intense.models import (
    Comment,CommentReply,
    Reviews,Order,
    OrderDetails,
    User,
    GroupProduct, 
    Product, 
    Variation, 
    Category,
    discount_product,
    ProductImpression,
    ProductImage,
    ProductCode,
    ProductPrice,
    ProductPoint,
    ProductSpecification,

    )

from django.http.response import JsonResponse
from django.contrib.auth import get_user_model
import django_filters.rest_framework
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from rest_framework.generics import ListAPIView 
from User_details.serializers import UserSerializer
from django.db.models import Q
from django.utils import timezone
from django.db import transaction
from Intense.Integral_apis import (
    product_data_upload,category_data_upload,product_price_data_upload,
    product_specification_data_upload,product_point_data_upload,
    create_product_code,product_discount_data_upload,product_image_data_upload,product_data_update,price_data_update,
    discount_data_update,point_data_update,specification_data_update,group_product_data_update,group_product_data_modification
)
from io import BytesIO 
import barcode
from barcode.writer import ImageWriter
from django.core.files.base import ContentFile
from PIL import Image
import PIL
from django.conf import settings
import os
from django.utils import timezone

# -------------------- Product -----------------------

@api_view(['GET',])
def display_products(request,number):


    latest = {}
    discount = {}
    popular = {}
    group={}
    current_date = timezone.now()


    try:
        
        latest_products = Product.objects.filter(is_deleted=False).order_by('date')
        #this fetches all the comment ids
        
    except:
        latest_products = None

   

    if latest_products:

        latest_products_serializer = ProductSerializer(latest_products,many=True)
        if(number>0):
            latest = latest_products_serializer.data[:number]
        else:
            latest = latest_products_serializer.data

    else: 

        latest = {}

    
    try:
        
        group_products = Product.objects.filter(is_group = True,is_deleted=False).order_by('date')
        #this fetches all the comment ids
        
    except:
        group_products = None

   

    if group_products:

        group_products_products_serializer = ProductSerializer(group_products,many=True)
        if(number>0):
            group = group_products_products_serializer.data[:number]
        else:
            group = group_products_products_serializer.data

    else: 

        group = {}


    try:


        # criterion1 = Q(start_date<=current_date)
        # print(criterion1)
        # criterion2 = Q(end_date>=current_date)
        # print(criterion2)

        product_discounts = discount_product.objects.filter(start_date__lte=current_date ,end_date__gte=current_date)

    except:
        product_discounts = None

    if product_discounts:


        discounted_product_ids = list(product_discounts.values_list('product_id',flat=True).distinct())
    
        try:
            

            discounted_products = Product.objects.filter(pk__in=discounted_product_ids, is_deleted=False)

        except:

            discounted_products = None


        if discounted_products:

            

            discounted_products_serializer = ProductSerializer(discounted_products,many=True)
            if(number>0):
                discount = discounted_products_serializer.data[:number]
            else:
                discount = discounted_products_serializer.data

        else:
            
            discount = {}

    else:
        discount = {}


    try:

        popular_products = ProductImpression.objects.order_by('-sales_count')[:number]
        #print(popular_products)

    except:

        popular_products = None

    if popular_products:

        #Fetch the product ids 
        product_ids = list(popular_products.values_list('product_id' , flat = True))

        try:

            pop_products = Product.objects.filter(pk__in = product_ids,is_deleted=False)

        except:

            pop_products = None


        if pop_products:


            popular_products_serializer = ProductSerializer(pop_products,many=True)
            if(number>0):
                popular = popular_products_serializer.data[:number]
            else:
                popular = popular_products_serializer.data

        else:

            popular = {}

    else:

        popular = {}
  
    data = [{'name':'New Arrivals','products':latest},{'name':'On Sale','products':discount},{'name':'Popular','products':popular},
    {'name':'group Product', 'products':group}]



    return Response({
                'success': True,
                'message': 'The values are shown below',
                'data': data 
                })


@api_view(['POST',])
def show_more(request):


    latest = {}
    discount = {}
    popular = {}
    group={}
    current_date = timezone.now()

    name = request.data.get('name')


    try:
        
        latest_products = Product.objects.filter(is_deleted=False).order_by('date')
        #this fetches all the comment ids
        
    except:
        latest_products = None

   

    if latest_products:

        latest_products_serializer = ProductSerializer(latest_products,many=True)
     
        latest = latest_products_serializer.data

    else: 

        latest = {}

    
    try:
        
        group_products = Product.objects.filter(is_group = True,is_deleted=False).order_by('date')
        #this fetches all the comment ids
        
    except:
        group_products = None

   

    if group_products:

        group_products_products_serializer = ProductSerializer(group_products,many=True)

        group = group_products_products_serializer.data

    else: 

        group = {}


    try:


        # criterion1 = Q(start_date<=current_date)
        # print(criterion1)
        # criterion2 = Q(end_date>=current_date)
        # print(criterion2)

        product_discounts = discount_product.objects.filter(start_date__lte=current_date ,end_date__gte=current_date)

    except:
        product_discounts = None

    if product_discounts:


        discounted_product_ids = list(product_discounts.values_list('product_id',flat=True).distinct())
    
        try:
            

            discounted_products = Product.objects.filter(pk__in=discounted_product_ids, is_deleted=False)

        except:

            discounted_products = None


        if discounted_products:

            

            discounted_products_serializer = ProductSerializer(discounted_products,many=True)

            discount = discounted_products_serializer.data

        else:
            
            discount = {}

    else:
        discount = {}


    try:

        popular_products = ProductImpression.objects.order_by('-sales_count')[:number]
        #print(popular_products)

    except:

        popular_products = None

    if popular_products:

        #Fetch the product ids 
        product_ids = list(popular_products.values_list('product_id' , flat = True))

        try:

            pop_products = Product.objects.filter(pk__in = product_ids,is_deleted=False)

        except:

            pop_products = None


        if pop_products:


            popular_products_serializer = ProductSerializer(pop_products,many=True)

            popular = popular_products_serializer.data

        else:

            popular = {}

    else:

        popular = {}
  
    # data = [{'name':'New Arrivals','products':latest},{'name':'On Sale','products':discount},{'name':'Popular','products':popular},
    # {'name':'group Product', 'products':group}]

    if name == "New Arrivals":
        data = [{'name': name,'products':latest}]

    elif name == "On Sale":
        data = [{'name': name,'products':discount}]

    elif name == "Popular":
        data = [{'name': name,'products':popular}]


    elif name == "group Product":
        data = [{'name': name,'products':group}]

  





    return Response({
                'success': True,
                'message': 'The values are shown below',
                'data': data 
                })
class ListReviewView(ListAPIView):
    queryset = Reviews.objects.all()
    serializer_class = ReviewsSerializer
    filter_backends = (
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    )
    search_fields = ("rating")
    filterset_fields = ['rating']
 
    
    @time_calculator
    def time(self):
        return 0

    @method_decorator(vary_on_cookie)
    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        serializer = self.get_serializer(queryset, many=True)
        self.time()
        return Response ({
            'success': True,
            'message': "Data has been retrived successfully",
            'data': serializer
            })
  

      


class ListProductView(ListAPIView):
    queryset = Product.objects.all()
    serializer_class = SearchSerializer
    filter_backends = (
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    )
    search_fields = ("title",'brand')
    filterset_fields = ['title', 'brand']

    @time_calculator
    def time(self):
        return 0

    @method_decorator(vary_on_cookie)
    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        serializer = self.get_serializer(queryset, many=True)
        self.time()
        return Response ({
            'success': True,
            'message': "Data has been retrived successfully",
            'data': serializer.data
        })

    


@api_view (["GET","post"])
def get_all_product(request):

 #"This api is for view all Product informations"
    if (request.method == "GET"):
        queryset = Product.objects.all()
        product_serializers = ProductSerializer(queryset , many = True)
        return Response (product_serializers.data)

@api_view (["GET" , "POST"])
#"This api is for view create  product.  "
def insert_specific_product_value(request):
    if(request.method == "POST"):
        product_serializers=ProductSerializer(data=request.data)
        if(product_serializers.is_valid()):
            product_serializers.save()
            return Response (product_serializers.data, status=status.HTTP_201_CREATED)
        return JsonResponse(product_serializers.errors)

@api_view(["GET","POST"])
def get_update_product_value(request , product_id):

	try:
		product = Product.objects.get(id=product_id)
		if request.method == 'POST':
			serializers = ProductSerializer(product , data=request.data )
			if serializers.is_valid():
				serializers.save()
				return JsonResponse(serializers.data)
			return JsonResponse(serializers.errors)

	except Product.DoesNotExist:
		return JsonResponse({'message': 'This product does not exist'}, status=status.HTTP_404_NOT_FOUND)



@api_view(['POST','GET'])
def delete_product_value(request ,product_id):
    '''
  This is for delete a specific Product
    ''' 
    try:
        product = Product.objects.filter(id =product_id)
    except:
        product = None

    if product is not None:
        product.delete()
        return JsonResponse({'message': 'Product was deleted successfully!'}, status=status.HTTP_204_NO_CONTENT)
    else:
        return JsonResponse({'message': 'Product was deleted successfully!'})

# ------------------------- Product Image ---------------------------------

@api_view (["GET" , "POST"])
def product_image_up(request):
    if(request.method == "POST"):
        try:
            values_data = request.data
            #print(values_data['image'])
            
            serializers=ProductImageSerializer(data=request.data)
            if(serializers.is_valid()):
                serializers.save()
                return Response (serializers.data, status=status.HTTP_201_CREATED)
            return Response(serializers.errors)
        except:
            return Response ({
                'success': False,
                'message': 'Some Internal problem occurs'
                        })

@api_view (["GET","post"])
def get_all_product_image(request):

    if (request.method == "GET"):
        try:
            queryset = ProductImage.objects.all()
            serializers = ProductImageSerializer(queryset , many = True)
            return Response (serializers.data)
        except:
            return Response({
                'success': False,
                'message': 'Some problem occurs while retriveing the data'
            })

@api_view (["GET","post"])
def get_specific_product_image(request, image_id):

    if (request.method == "GET"):
        try:
            queryset = ProductImage.objects.get(id = image_id)
            serializers = ProductImageSerializer(queryset , many = False)
            return Response (serializers.data)
        except:
            return Response({
                'success': False,
                'message': 'Requested data can not be found'
            })

@api_view(["GET","POST"])
def update_product_image_value(request, image_id):

    try:
        product_img = ProductImage.objects.get(id=image_id)
    except:
        return JsonResponse({'message': 'Image does not exists'}, status=status.HTTP_404_NOT_FOUND)

        if request.method == 'POST':
            serializers = ProductImageSerializer(product_img , data=request.data )
            if serializers.is_valid():
                serializers.save()
                return JsonResponse(serializers.data)
            return JsonResponse(serializers.errors, status=status.HTTP_400_BAD_REQUEST)




@api_view (["GET","post"])
def delete_specific_product_image(request, image_id):

    if (request.method == "POST"):
        try:
            queryset = ProductImage.objects.get(id = image_id)
            queryset.delete()
            return Response ({'Message': ' data has been deleted successfully'})
        except:
            return Response ({
                'success': False,
                'Message': 'Data could not be deleted'})

@api_view (["GET","post"])
def get_all_product_category(request):

    if (request.method == "GET"):
        queryset = Category.objects.all()
        serializers = CategorySerializer(queryset , many = True)
        return Response (serializers.data)

@api_view (["GET" , "POST"])
def insert_specific_category_value(request):
    if(request.method == "POST"):
        serializers=CategorySerializer(data=request.data)
        if(serializers.is_valid()):
            serializers.save()
            return Response (serializers.data, status=status.HTTP_201_CREATED)
        return JsonResponse(serializers.errors)


@api_view(["GET","POST"])
def get_update_category_value(request, category_id):

	try:
		product = Category.objects.get(id=category_id)
		if request.method == 'POST':
			serializers = CategorySerializer(product , data=request.data )
			if serializers.is_valid():
				serializers.save()
				return JsonResponse(serializers.data)
			return JsonResponse(serializers.errors, status=status.HTTP_400_BAD_REQUEST)

	except Product.DoesNotExist:
		return JsonResponse({'message': 'This Category does not exist'}, status=status.HTTP_404_NOT_FOUND)
@api_view(['POST','GET'])
def delete_category_value(request , category_id):

    try:
        category = Category.objects.filter(id =category_id)
    except:
        category = None

    if category is not None:
        category.delete()
        return JsonResponse({'message': 'Category was deleted successfully!'}, status=status.HTTP_204_NO_CONTENT)
    else:
        return JsonResponse({'message': 'Category was not deleted successfully!'})



@api_view (["GET","post"])
def get_all_group_product(request):
 
    if (request.method == "GET"):
        queryset = GroupProduct.objects.all()
        serializers = GroupProductSerialyzer(queryset , many = True)
        return Response (serializers.data)

@api_view (["GET" , "POST"])
def insert_specific_group_product_value(request):

  

    if(request.method == "GET"):
        return Response({''})

    if(request.method == "POST"):
        serializers=GroupProductSerialyzer(data=request.data)
        if(serializers.is_valid()):
            serializers.save()
            return Response (serializers.data, status=status.HTTP_201_CREATED)
        return Response(serializers.errors)

@api_view(["GET","POST"])
def get_update_group_product_value(request , product_id):
   
    try:
        product = GroupProduct.objects.get(id=product_id)
    except Product.DoesNotExist:
        return JsonResponse({'message': 'This Group does not exist'}, status=status.HTTP_404_NOT_FOUND)
        
    if request.method == 'GET':
        serializers = GroupProductSerialyzer(product , many = False)
        return Response (serializers.data)
    if request.method == 'POST':
        serializers = GroupProductSerialyzer(product , data=request.data )
        if serializers.is_valid():
            serializers.save()
            return JsonResponse(serializers.data)
        return JsonResponse(serializers.errors, status=status.HTTP_400_BAD_REQUEST)

	


@api_view(['POST','GET'])
def delete_group_product_value(request, gp_id):
    '''
   
    ''' 
    try:
        product = GroupProduct.objects.filter(id=gp_id)
    except:
        product = None

    if product is not None:
        product.delete()
        return JsonResponse({'message': 'Your Group Product was deleted successfully!'}, status=status.HTTP_204_NO_CONTENT)
    else:
        return JsonResponse({'message': 'Group Product was deleted successfully!'})



#------------Product comments and reviews----------------------------

#Display the comments and replies of a specific product of a specific product
@api_view(['GET',])
def comments_product(request,product_id):

     try:
        comments = Comment.objects.filter(product_id = product_id)
        #this fetches all the comment ids
        comment_ids = comments.values_list('id' , flat = True)
        replies = []
        for i in range(len(comment_ids)):
            comment_data = CommentReply.objects.filter(comment_id=comment_ids[i])
            replies += comment_data

        if request.method == 'GET':
            commentserializer = CommentSerializer(comments , many=True)
            #replyserializer = CommentReplySerializer(replies , many = True)
            #comments = [commentserializer.data,replyserializer.data]
            return JsonResponse(commentserializer.data , safe=False)



        
     except Comment.DoesNotExist:
        return JsonResponse({'message': 'This comment does not exist'}, status=status.HTTP_404_NOT_FOUND)


# @api_view(['GET',])
# def comments(request,product_id):

#   try:
#       comments = Comment()
#       comments.product_id = product_id
#       comments = Comment.objects.filter(product_id = product_id).first()
#       if request.method == 'GET':
#           commentserializer = CommentSerializer(comments)
#           return JsonResponse(comments,safe= False)

#   except Comment.DoesNotExist:
#       return JsonResponse({'message': 'This comment does not exist'}, status=status.HTTP_404_NOT_FOUND)








#This creates a comment
@api_view(['POST',])
def create_comment(request):

    if request.method == 'POST':
        commentserializer = CommentSerializer(data=request.data)
        if commentserializer.is_valid():
            commentserializer.save()
            return JsonResponse(commentserializer.data, status=status.HTTP_201_CREATED)
        return JsonResponse(commentserializer.errors)

User = get_user_model()
#This creates a reply
@api_view(['POST',])
def create_reply(request):

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
            
            names = User.objects.filter(id=user_id).last()
         
            
            
        except:
            names = None

        if names is not None:

            
            reply_name = str(names.username)

            reply = CommentReply.objects.create(name = reply_name)
            reply.save()
            replyserializer = CommentReplySerializer(reply,data=request.data)
            if replyserializer.is_valid():
                replyserializer.save()
                return JsonResponse(replyserializer.data, status=status.HTTP_201_CREATED)
            return JsonResponse(replyserializer.errors)

        else:
            
            replyserializer = CommentReplySerializer(data=request.data)
            if replyserializer.is_valid():
                replyserializer.save()
                return JsonResponse(replyserializer.data, status=status.HTTP_201_CREATED)
            return JsonResponse(replyserializer.errors)

    else:
        name = "Anonymous"
        reply = CommentReply.objects.create(name = name)
        reply.save()
        replyserializer = CommentReplySerializer(reply,data=request.data)
        if replyserializer.is_valid():
            replyserializer.save()
            return JsonResponse(replyserializer.data, status=status.HTTP_201_CREATED)









#This edits an existing comment
@api_view(['POST',])
def edit_comment(request,comment_id):

    try:
        comment = Comment.objects.get(pk = comment_id)
        if request.method == 'POST':
            commentserializer = CommentSerializer(comment , data=request.data )
            if commentserializer.is_valid():
                commentserializer.save()
                return JsonResponse(commentserializer.data)
            return JsonResponse(commentserializer.errors)


    except Comment.DoesNotExist:
        return JsonResponse({'message': 'This comment does not exist'}, status=status.HTTP_404_NOT_FOUND)



#This edits a reply
@api_view(['POST',])
def edit_reply(request,reply_id):

    try:
        reply = CommentReply.objects.get(pk = reply_id)
        if request.method == 'POST':
            replyserializer = CommentReplySerializer(reply , data=request.data )
            if replyserializer.is_valid():
                replyserializer.save()
                return JsonResponse(replyserializer.data)
            return JsonResponse(replyserializer.errors)

                
    except CommentReply.DoesNotExist:
        return JsonResponse({'message': 'This reply does not exist'}, status=status.HTTP_404_NOT_FOUND)


#This deletes all the comments and the replies of that comment 
@api_view(['POST',])
def delete_comment(request,comment_id):

    try:
        comment = Comment.objects.filter(id = comment_id)
        replies = CommentReply.objects.filter(comment_id = comment_id)
        if request.method == 'POST':
            comment.delete()
            replies.delete()
            return JsonResponse({'message': 'The comment and its replies were deleted successfully!'}, status=status.HTTP_204_NO_CONTENT)




    except Comment.DoesNotExist:
        return JsonResponse({'message': 'This comment does not exist'}, status=status.HTTP_404_NOT_FOUND)




@api_view(['POST',])
def delete_reply(request,reply_id):

    try:
        
        replies = CommentReply.objects.filter(id = reply_id)
        if request.method == 'POST':
            
            replies.delete()
            return JsonResponse({'message': 'The reply was deleted successfully!'}, status=status.HTTP_204_NO_CONTENT)




    except Comment.DoesNotExist:
        return JsonResponse({'message': 'This reply does not exist'}, status=status.HTTP_404_NOT_FOUND)


#Fetches all the reviews of a certain product   
@api_view(['GET',])
def reviews_product(request,product_id):

    try:
        reviews = Reviews.objects.filter(product_id = product_id)
    except:
        reviews = None

    if reviews is None:

        return JsonResponse({})

    else:

        reviewsserializer = ReviewsSerializer(reviews,many=True)
        return JsonResponse(reviewsserializer.data , safe=False)


 



#This creates a review
@api_view(['POST',])
def create_review(request):

    user_id = request.data.get('user_id')
    non_verified_user_id = request.data.get('non_verified_user_id')
    product_id = request.data.get('product_id')
    product_id = int(product_id)
    print(product_id)
    if user_id is not None:
        user_id = int(user_id)
        non_verified_user_id =0

    else:
        non_verified_user_id = int(non_verified_user_id)
        user_id = 0

    if non_verified_user_id == 0:
        #The user is a verified user 

        #checking if the user has purchased the following product

        #Checking if orders exist of this user 
        flag = True
    
        
        try: 
            orders = Order.objects.filter(user_id=user_id,checkout_status=True,delivery_status="Received",order_status="Paid")
            
        except:
            orders = None

        if orders is not None:
            
            order_ids = orders.values_list('id' , flat = True)
            
            for i in range(len(order_ids)):
                orderdetails = OrderDetails.objects.filter(order_id=order_ids[i],is_removed=False)
                product_ids = orderdetails.values_list('product_id',flat= True)
                

                
                if (product_id in product_ids):
                    flag = False
                    break

            if flag == True:
                
                return JsonResponse({'message': 'You cant review this product because you din not buy it'})

            else:
                
                reviewserializer = ReviewsSerializer(data=request.data)
                if reviewserializer.is_valid():
                    reviewserializer.save()
                return JsonResponse(reviewserializer.data)


        else:
            return JsonResponse({'message': 'You cant review this product because you din not buy it'})

    else:   


        flag = True
    
        
        try: 
            orders = Order.objects.filter(non_verified_user_id=non_verified_user_id,checkout_status=True,delivery_status="Received",order_status="Paid")

        except:
            orders = None

        if orders is not None:
            order_ids = orders.values_list('id' , flat = True)
            for i in range(len(order_ids)):
                orderdetails = OrderDetails.objects.filter(order_id=order_ids[i],is_removed=False)
                product_ids = orderdetails.values_list('product_id',flat= True)
                if (product_id in product_ids):
                    flag = False
                    break

            if flag == True:
                return JsonResponse({'message': 'You cant review this product because you din not buy it'})

            else:
                reviewserializer = ReviewsSerializer(data=request.data)
                if reviewserializer.is_valid():
                    reviewserializer.save()
                return JsonResponse(reviewserializer.data)

        else:
            return JsonResponse({'message': 'You cant review this product because you din not buy it'})


        

        
#This edits an existing review
@api_view(['POST',])
def edit_review(request,review_id):

    try:
        reply = Reviews.objects.get(pk= review_id)
    except:
        reply = None
    if reply is not None:

        replyserializer = ReviewsSerializer(reply , data=request.data )
        if replyserializer.is_valid():
            replyserializer.save()
            return JsonResponse(replyserializer.data)
        return JsonResponse(replyserializer.errors)
        
     

    else:
        return JsonResponse({'message': 'The review does not exist!'})


                
    
        

#This deleted a review
@api_view(['POST',])
def delete_review(request,review_id):

    try:
        
        reviews = Reviews.objects.filter(id = review_id)
        if request.method == 'POST':
            
            reviews.delete()
            return JsonResponse({'message': 'The review was deleted successfully!'}, status=status.HTTP_204_NO_CONTENT)




    except Reviews.DoesNotExist:
        return JsonResponse({'message': 'This review does not exist'}, status=status.HTTP_404_NOT_FOUND)

# ------------------------------- Product Code -------------------------

@api_view (["GET","POST"])
def get_specific_code_values(request,product_id,height,width):
    '''
    This Api is for getting an individual product code. Calling http://127.0.0.1:8000/code/value/product_id/150/250
    will cause to invoke this API. While getting values, user may specify the image size in which user expects it. This valu need to be passed
    as a parameter.

        GET Response:
            While performing get response this API will give a JSON response. As a response it will provide the following data.
            Barcode_img : (barcode will be an image. While retreiving this will be the url of the barcode image.)
            Date : (This is the date on wchich the product code is been created.)
            Barcode : This will be the product barcode. Based on this later, the product can be found.
    '''
  

    if(request.method == "GET"):
        try:
            queryset = ProductCode.objects.get(product_id = product_id)
            resized = Image.open(queryset.Barcode_img) 
            newSize = (width , height )
            # Getting barcode url and before retreiving it resizes the barcode as per the user specification
            resized = resized.resize(newSize, resample=PIL.Image.NEAREST)
            resized.save(settings.MEDIA_DIR+'/barcode/'+ str(product_id)+'.png')
            url = settings.MEDIA_DIR+'/barcode/' + str(product_id)+'.png'
            code_serializers = ProductCodeSerializer (queryset, many = False)
            return Response (code_serializers.data)
        except:
            return Response({'message': 'Thre is no value to retrive'})

@api_view (["GET","POST"])
def insert_specific_code_values(request):
    '''
    This is for creating barcode for a particular product and insert it into the database. Calling http://127.0.0.1:8000/code/insert_value/ will 
    cause to invoke this API. This api has just post response.

    POST Response:
        While performing post response this api requires just the product id. Based on that product id this api will generate the product code 
        and will save the code as an image data into the media folder. At a same time it will store the image url into database Barcode field.
    
    '''
    if request.method == "POST":
        # demo values
        values = request.data

        bar = barcode.get_barcode_class('code39')
        bar_value = bar(str(values['product_id']), writer = ImageWriter())

        if not os.path.exists(settings.MEDIA_DIR+'/barcode/'):
            os.makedirs(settings.MEDIA_DIR+'/barcode/')
        bar_value.save(settings.MEDIA_DIR+'/barcode/'+ str(values['product_id']))
        url = settings.MEDIA_DIR+'/barcode/' + str(values['product_id'])+'.png'

        data_values  = {'product_id' : values['product_id'], 'Barcode_img' : url, 'Barcode' : str((values['product_id'])) }

        code_serializer_value = ProductCodeSerializer (data= data_values)
        if(code_serializer_value.is_valid()):
            code_serializer_value.save()
            return Response (code_serializer_value.data, status=status.HTTP_201_CREATED)
        return Response (code_serializer_value.errors)


@api_view (["GET","POST"])
def specific_code_delete(request):
    '''
    This Api is for deleting a particular product value. While performing the delete operation it expects a particualr product id. 
    Calling http://127.0.0.1:8000/code/delete_value/ will cause to invoke this API.
    '''
    #demo value
    values = {'product_id': '12'}

    try:
        specific_data = ProductCode.objects.get(product_id = values['product_id'])
    except :
        return Response({'message': 'There is no value to delete'})
    
    if request.method == "POST":
        specific_data.delete()
        os.remove(specific_data.Barcode_img)
        return Response({'message': ' Value is successfully  deleted'}, status=status.HTTP_204_NO_CONTENT)


@api_view (["GET","POST"])
def get_product_using_barcode (request,scanned_code):
    '''
    This API is for getting product id condition on passing scanned value as a parameters. This will be required while scanner will send the scanned barcode.
    Based on the scanned code this Api will provide corresponding product Id. Calling http://127.0.0.1:8000/code/scanned_value/12/ will cause to invoke this ApI.
    This will have just Get response.

    Get Response:
    Followings data will be provided while performing the get response.
    scan_product_id : This will be the product id which was scanned through the scanner. This product id will be required later to find the product details.
    date : The date on which the product barcode was created.
    '''

    if request.method == 'GET':
        try:
            specific_data = ProductCode.objects.get(Barcode = scanned_code)
            data_serializers = ScannerProductSerializer (specific_data)
            return Response (data_serializers.data)
        except:
            return Response({'message': 'There is no value'})


#This api is used to get the total rating count for a product,the average rating and how much of each rating does this product have
@api_view(['GET',])
def product_ratings(request,product_id):

    try:
        product = Reviews.objects.filter(product_id=product_id).first()
    except:
        product = None

    if product is None:
        return JsonResponse({})

    else:

        productserializer = ProductReviewSerializer(product,many=False)
        return JsonResponse(productserializer.data,safe=False)

   


@api_view(['POST',])
def upload_product(request):

    # arr={
    #     "seller_id": "18",
    #     "title": "Samsung360",
    #     "description": "This is a good product",
    #     "quantity": "3",
    #     "brand": "Samsung",
    #     "key_feature": ["This is a good product","Nice nice","good good"],
        
    #     }

    # data = request.data
    # title = data['title']
    # description = data['description']
    # brand = data['brand']
    # key_feature = data['key_feature']


    # product = Product.objects.create(title=title,description=description,brand=brand)

    # product.save()
    # product.



    product_serializer = CreateProductSerializer(data=request.data)
    if product_serializer.is_valid():
        product_serializer.save()
        return JsonResponse(product_serializer.data)
    return JsonResponse(product_serializer.errors)



@api_view(['POST',])
def edit_product(request,product_id):

    try:

        product = Product.objects.filter(id= product_id).last()

    except:
        product = None

    if product is not None:

        product_serializer = CreateProductSerializer(data=request.data)
        if product_serializer.is_valid():
            product_serializer.save()
            return JsonResponse(product_serializer.data)
        return JsonResponse(product_serializer.errors)

    else:
        JsonResponse({'message': 'This product does not exist'})



@api_view(['POST',])
def specific_product_update(request,product_id):
    if request.method == 'POST':
        product_data = Product.objects.get(id = product_id)
        product_serializer = CreateProductSerializer(product_data, data=request.data)
        if product_serializer.is_valid():
            product_serializer.save()
            return JsonResponse(product_serializer.data)
        return JsonResponse(product_serializer.errors)


@api_view(['GET',])
def all_product_detail(request):

    product = Product.objects.all()
    product_serializer = ProductDetailSerializer(product,many= True)
    return JsonResponse({'success':True,'message':'The data is shown below','data':product_serializer.data},safe=False)
    

	# else:
	# 	return JsonResponse({'success':False,'message':'This product does not exist','data':''}, status=status.HTTP_404_NOT_FOUND)


@api_view(['POST','GET'])
def product_insertion_admin(request):

    # print(request.data)
    data = request.data
    # data = request.body
    



    

    # im = data['images']

    print(len(data))

    count = len(data)-13
    print(count)

    key_features = request.data.get("key_features")
    # print(key_features)
    # print(key_features)

    
    # li = list(key_features.split(",")) 
    # print(li)
    
    # key_feature = key_features.split(",")
    # features = []
    # for i in range(len(key_feature)):
    #     print(key_feature[i])
    #     features.append(key_feature[i])
   
    date = timezone.now().date()

    # print(request.data['brand'])
  


    
    features = key_features.split(",")
    # print(features)

    

  
    product_data_value ={

            
            'title': request.data.get("title"),
            'brand': request.data.get("brand"),
            'description':request.data.get("description"),
            'key_features':features,
            'is_deleted': False,
            'properties': True
        }

    category_data_value ={

            
            'category': request.data.get("category"),
            'sub_category': request.data.get("sub_category"),
            'sub_sub_category': request.data.get("sub_sub_category")
        }


   
    product_price ={
        'price' : request.data.get("price"),
        #'currency_id': request.data.get('currency_id')
    }

    # product_specification= [
    #     {
    #     "weight": request.data.get('weight'),
    #     "color":request.data.get('color'),
    #     "size":request.data.get('size'),
    #     'quantity': request.data.get('quantity')
    #    },
    #     {
        
    #     "color":'Green',
    #     "size":'Large',
    #     'quantity': 20
    #    },
    #     {
        
    #     "color":'Blue',
    #     "size":'XXL',
    #     'quantity': 7
    #    }
    # ]




    product_point ={
        'point': request.data.get("point"),
        # 'end_date': data['point_end_date']
        'end_date': date
    }

    product_discount ={

        'amount': request.data.get("amount"),
        #'start_date' : '2020-09-05',
        #'end_date' : data['discount_end_date']
        'end_date':date
    }

    # product_image=[
        
    #          'This is image 1', 'This is image 2', 'This is image 3', 'This is image 4'
    # ]

 

    if request.method == 'POST':
        
        try:
            #print("dbcudbfdbcducbducbducbducbd")
            category_values= category_data_upload (category_data_value)
            print("1")
            #print(category_values)
            category_data = category_values.json()
            print("2")
            #print(category_data)
            category_id = category_data['category']
            sub_category_id = category_data['sub_category']
            sub_sub_category_id = category_data['sub_sub_category']
            product_data_value.update( {'category_id' : category_id,'sub_category_id' : sub_category_id,'sub_sub_category_id' : sub_sub_category_id} )
            print("3")
            product_values= product_data_upload (product_data_value)
            print("4")
            product_data= product_values.json()
            product_id = product_data['id']
            product_price.update( {'product_id' : product_id} )
            print("5")
            price_values = product_price_data_upload (product_price)
            product_point.update ({'product_id' : product_id})
            print("6")
            point_values = product_point_data_upload(product_point)
            product_code = create_product_code({'product_id' : product_id})
            print("7")
            product_discount.update({'product_id' : product_id})
            discount_data = product_discount_data_upload(product_discount)
            print("8")

            for i in range(int(count)):
                print(i)
                dataz = request.data
                image = dataz['images['+str(i)+']']
                print("aaaaaaaaaaaaaaaaaaa")
                print(image)
                image_data = {'product_image':image}
                
                product_image = ProductImage.objects.create(product_image=image,product_id=product_id)
                product_image.save()
                print(product_image)
                product_image_serializer = ProductImageSerializer(product_image,data=image_data)

                if product_image_serializer.is_valid():
                    product_image_serializer.save()
                    print("saved")
                    
            #product_img =[]
            #product_spec=[]
            # for img in product_image:
            #     data = {'content':img}
            #     data.update({'product_id' : product_id})
            #     img_data= product_image_data_upload(data)
            #     product_img.append(img_data.json())


            # for spec in product_specification:
            #     spec.update({'product_id' : product_id})            
            #     product_sp = product_specification_data_upload (spec)
            #     product_spec.append(product_sp.json())
        
            return Response({
                
                'success': True,
                'product_data': product_data,
                'price_values': price_values.json(),
                #'product_specification': product_spec,
                'product_point': point_values.json(),
                'product_code': product_code.json(),
                'product_discount': discount_data.json(),
                # 'product_image': product_img
            }) 
        except:

            product_price = ProductPrice.objects.filter(product_id = product_id)
            if product_price.exists():
                product_price.delete()

            product_discount = discount_product.objects.filter(product_id = product_id)
            if product_discount.exists():
                product_discount.delete()

            product_code = ProductCode.objects.filter(product_id = product_id)
            if product_code.exists():
                product_code.delete()

            product_point = ProductPoint.objects.filter(product_id = product_id)
            if product_point.exists():
                product_point.delete()

            # product_specification = ProductSpecification.objects.filter(product_id = product_id)
            # if product_specification.exists():
            #     product_specification.delete()
            
            product_image = ProductImage.objects.filter(product_id = product_id)
            if product_image.exists():
                product_image.delete()
            
            product_value = Product.objects.filter(id = product_id)
            if product_value.exists():
                product_value.delete()
            
            return Response({
                'success': False,
                'message': 'Product insertion could not be completed'
                })

            


@api_view(['POST','GET'])
def specific_product_delete_admin(request, product_id):

    if request.method == 'POST':

        try:
        
            product_value = Product.objects.get(id = product_id) 
            product_price = ProductPrice.objects.filter(product_id = product_id)
            product_discount = discount_product.objects.filter(product_id  = product_id)  
            product_code = ProductCode.objects.filter(product_id  = product_id)
            product_point = ProductPoint.objects.filter(product_id = product_id)
            product_specification = ProductSpecification.objects.filter(product_id  = product_id)
            product_image = ProductImage.objects.filter(product_id  = product_id)

           
            product_value.delete()
            if product_image.exists():
                product_image.delete()
            if product_price.exists():
                product_price.delete()
            if product_discount.exists():
                product_discount.delete()
            if product_code.exists():
                product_code.delete()
            if product_point.exists():
                product_point.delete()
            if product_specification.exists():
                product_specification.delete()

            return Response({
                'success': True,
                'message': 'Product has been deleted successfully'
            })
        
        except:
            return Response({
                'success': False,
                'message': 'Product could not be deleted successfully'
            })


@api_view(['POST','GET'])
def specific_product_hidden_delete(request, product_id):

    if request.method == 'POST':
        try:
            product_value = Product.objects.get(id = product_id) 
            product_value.is_deleted = True
            data = product_value.__dict__
            product_data_update(product_id, data)
            return Response({
                    'success': True,
                    'message': 'Product has been deleted successfully'
                })
        
        except:
            return Response({
                'success': False,
                'message': 'Product could not be deleted successfully'
            })


@api_view(['POST','GET'])
def modify_specific_product(request, product_id):
    data = request.data
    # product_values = {'title':'puffed rice'}
    # price_values = {'price': 150}
    # discount_values = {'amount': 30}
    # point_values = {'point': 20}
    # specification_values = {
    #         'color': 'blue'}

    product_data_value ={

            
            'title': data['title'],
            'brand': data['brand'],
            'description': data['description'],
            'key_features':data['key_features'],
            'is_deleted': False,
            'properties': True
        }

    category_data_value ={

            
            'category': data['category'],
            'sub_category': data['sub_category'],
            'sub_sub_category': data['sub_sub_category']

        }


   
    product_price ={
        'price' : data['price'],
        #'currency_id': request.data.get('currency_id')
    }

    # product_specification= [
    #     {
    #     "weight": request.data.get('weight'),
    #     "color":request.data.get('color'),
    #     "size":request.data.get('size'),
    #     'quantity': request.data.get('quantity')
    #    },
    #     {
        
    #     "color":'Green',
    #     "size":'Large',
    #     'quantity': 20
    #    },
    #     {
        
    #     "color":'Blue',
    #     "size":'XXL',
    #     'quantity': 7
    #    }
    # ]




    product_point ={
        'point': data['point'],
        # 'end_date': data['point_end_date']
        'end_date': date
    }

    product_discount ={

        'amount': data['amount'],
        #'start_date' : '2020-09-05',
        #'end_date' : data['discount_end_date']
        'end_date':date
    }

    # product_image=[
        
    #          'This is image 1', 'This is image 2', 'This is image 3', 'This is image 4'
    # ]

    if request.method == 'POST':
        
        try:
            
            product_data = product_data_update(product_id, product_data_value)
            price_data = price_data_update (product_id, price_values)
            discount_data = discount_data_update (product_id,discount_values)
            point_data = point_data_update (product_id,point_values)
            specification_data = specification_data_update(product_id, specification_values)

            return Response({
                'success': True,
                'product': product_data.json(),
                'price': price_data.json(),
                'discount':discount_data.json(),
                'point': point_data.json(),
                'specification': specification_data.json()

            })

        except:
            return Response({
                'success': False,
                'message': 'Product modification could not be updated'
               
            })


@api_view(['POST','GET'])
def group_product_insertion_admin(request):
    '''
    This Api is for inserting all the group related information by using a single API. This will be for the admin. Calling 
    http://127.0.0.1:8000/product/group_product_insert/ will cause to invoke this Api. 
    '''
  
    product_data_value ={

            
            'title': 'Bundle Offer',
            'brand': 'mix',
            'description': 'World famous product',
            'key_featues': 'all are special',
            'quantity': 10,
            'is_deleted': False,
            'properties': True,
            'is_group':True
        }

    group_product_values=   {
    
            "products_ids": [1,2,3,4],
            "title": "nothing to doesswer",
            "product_id": 2
        }

    product_price ={
        'price' : '350',
        'currency_id': '1'
    }

  #   product_specification= [
  #       {
		# "weight": '17',
		# "color":'red',
		# "size":'small',
  #       'quantity': 10
  #      },
  #       {
		
		# "color":'Green',
		# "size":'Large',
  #       'quantity': 20
  #      },
  #       {
		
		# "color":'Blue',
		# "size":'XXL',
  #       'quantity': 7
  #      }
  #   ]

    product_point ={
        'point': '80'
    }

    product_discount ={

        'amount': 5,
        'start_date' : '2020-09-05',
        'end_date' : '2020-09-25'
    }

    product_image=[
        
             'This is image 1', 'This is image 2', 'This is image 3', 'This is image 4'
    ]

    

    if request.method == 'POST':
        try:
            product_values= product_data_upload (product_data_value)
            product_data= product_values.json()
            product_id = product_data['id']
            
            group_product_values.update( {'product_id' : product_id} )
            group_values = group_product_data_update (group_product_values)
            product_price.update( {'product_id' : product_id} )
            price_values = product_price_data_upload (product_price)
            product_point.update ({'product_id' : product_id})
            point_values = product_point_data_upload(product_point)
            product_code = create_product_code({'product_id' : product_id})
            product_discount.update({'product_id' : product_id})
            discount_data = product_discount_data_upload(product_discount)
            product_img =[]
            product_spec=[]
            
            for img in product_image:
                data = {'content':img}
                data.update({'product_id' : product_id})
                img_data= product_image_data_upload(data)
                product_img.append(img_data.json())
            
            for spec in product_specification:
                spec.update({'product_id' : product_id})            
                product_sp = product_specification_data_upload (spec)
                product_spec.append(product_sp.json())
        
            return Response({
                'success': True,
                'product_data': product_data,
                'group_values': group_values.json(),
                'price_values': price_values.json(),
                'product_specification': product_spec,
                'product_point': point_values.json(),
                'product_code': product_code.json(),
                'product_discount': discount_data.json(),
                'product_image': product_img
            }) 
        except:

            product_price = ProductPrice.objects.filter(product_id = product_id)
            if product_price.exists():
                product_price.delete()

            group_product = GroupProduct.objects.filter(product_id = product_id)
            if group_product.exists():
                group_product.delete()

            product_discount = discount_product.objects.filter(product_id = product_id)
            if product_discount.exists():
                product_discount.delete()

            product_code = ProductCode.objects.filter(product_id = product_id)
            if product_code.exists():
                product_code.delete()

            product_point = ProductPoint.objects.filter(product_id = product_id)
            if product_point.exists():
                product_point.delete()

            product_specification = ProductSpecification.objects.filter(product_id = product_id)
            if product_specification.exists():
                product_specification.delete()
            
            product_image = ProductImage.objects.filter(product_id = product_id)
            if product_image.exists():
                product_image.delete()
            
            product_value = Product.objects.filter(id = product_id)
            if product_value.exists():
                product_value.delete()
            
            return Response({
                'success': False,
                'message': 'Group Product could not be inserted'
                })
            
@api_view(['POST','GET'])
def modify_specific_group_product(request, product_id):
    '''
    This is for modifying specific group product using a single Api. Calling the http://127.0.0.1:8000/product/modify_group_product/3/ will cause to
    invoke this Api.
    prams: product_id
    '''
    product_values = {'title':'puffed rice'}
    price_values = {'price': 150}
    discount_values = {'amount': 30}
    point_values = {'point': 20}
    specification_values = {
            'color': 'a'}

    group_product_values=   {

        "products_ids": [1,2,25],
        "title": "Have some days",
    }

    if request.method == 'GET':
        try:
             product = Product.objects.get(id=product_id)
        except:
            return JsonResponse({
                'success':False,
                'message':'Data could not be retrived'
            })

        product_serializer = AllGroupProductSerialyzer(product,many= False)
        return JsonResponse({
            'success':True,
            'message':'The data is shown below',
            'data':product_serializer.data},safe=False)


    if request.method == 'POST':
        
        try:
            
            product_data = product_data_update(product_id, product_values)
            group_data= group_product_data_modification(product_id,group_product_values)
            price_data = price_data_update (product_id, price_values)
            discount_data = discount_data_update (product_id,discount_values)
            point_data = point_data_update (product_id,point_values)
            specification_data = specification_data_update(product_id, specification_values)

            # return Response({
            #     'success': True,
            #     'product': product_data.json(),
            #     'price': price_data.json(),
            #     'discount':discount_data.json(),
            #     'point': point_data.json(),
            #     'specification': specification_data.json(),
            #     'group': group_data.json()

            # })

            return Response({
                'success': True,
                'product': product_data.json(),
                'price': price_data.json(),
                'discount':discount_data.json(),
                'point': point_data.json(),
                'specification': specification_data.json(),
                # 'group': group_data.json()

            })

        except:
            return Response({
                'success': False,
                'message': 'Data could not be updated'
               
            })


@api_view(['POST','GET'])
def get_all_detailed_group_product(request, number = 0):
    '''
    This is for showing all the group product together. An individual may send request to show the specific amount of details by sending the 
    expected number in the parameters. Number less than 0 will cause to show all the group product details.
    calling http://127.0.0.1:8000/product/all_group_product/2/ will cause to invoke this Api.

    parms: number

    '''
    
    if request.method == 'GET':
        try:
            products = Product.objects.all()
            product_serializer = AllGroupProductSerialyzer(products,many= True)
            if number>0:
                return Response({
                    'success': True,
                    'message':'Data has been retrived successfully',
                    'data':product_serializer.data[:number]
                })
            else:
                return Response({
                    'success': True,
                    'message':'Data has been retrived successfully',
                    'data':product_serializer.data
                })

        except:
            return Response({
                    'success': False,
                    'message':'Data could not be retrived',
                })
            

        
            

