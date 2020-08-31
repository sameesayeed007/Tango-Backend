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


from Intense.models import Category, Product, GroupProduct , Variation
# from user_profile.models import User

from .serializers import (
		CategorySerializer, 
		ProductSerializer,
        VariationSerializer,
        GroupProductSerialyzer,
        CreateProductSerializer
		)

from .decorators import time_calculator
from Intense.models import Comment,CommentReply,Reviews,Order,OrderDetails,User,GroupProduct, Product, Variation, Category 
from .serializers import CommentSerializer, CommentReplySerializer,ReviewsSerializer ,ProductReviewSerializer
from django.http.response import JsonResponse
from django.contrib.auth import get_user_model
import django_filters.rest_framework
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from rest_framework.generics import ListAPIView 
from User_details.serializers import UserSerializer

# -------------------- Product -----------------------


class ListProductView(ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = (
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    )
    search_fields = ("title",'brand')
    filterset_fields = ['title', 'brand']
    


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
def get_update_group_product_value(request , gp_id):

    try:
        product = GroupProduct.objects.get(id=gp_id)
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
        if request.method == 'GET':
            reviewsserializer = ReviewsSerializer(reviews,many=True)
            return JsonResponse(reviewsserializer.data , safe=False)


    except Reviews.DoesNotExist:
        return JsonResponse({'message': 'This review does not exist'}, status=status.HTTP_404_NOT_FOUND)



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


#This api is used to get the total rating count for a product,the average rating and how much of each rating does this product have
@api_view(['GET',])
def product_ratings(request,product_id):

    try:
        product = Reviews.objects.filter(product_id=product_id).last()
        productserializer = ProductReviewSerializer(product,many=False)
        return JsonResponse(productserializer.data,safe=False)

    except Reviews.DoesNotExist:
        return JsonResponse({'message': 'This review does not exist'}, status=status.HTTP_404_NOT_FOUND)


@api_view(['POST',])
def upload_product(request):

    arr={
        "seller_id": "18",
        "title": "Samsung360",
        "description": "This is a good product",
        "quantity": "3",
        "brand": "Samsung",
        "key_feature": ["This is a good product","Nice nice","good good"],
        
        }

    product_serializer = CreateProductSerializer(data=arr)
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