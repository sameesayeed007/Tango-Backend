import logging
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


from Intense.models import Category, Product, ProductViews, GroupProduct , Variation
# from user_profile.models import User
from .serializers import (
    CategoryListSerializer,
    ProductSerializer,
    SerpyProductSerializer,
    CreateProductSerializer,
    ProductViewsSerializer,
    ProductDetailSerializer,
    GroupProductSerializer,
)
from .permissions import IsOwnerAuth, ModelViewSetsPermission
from .decorators import time_calculator
from django.contrib.auth.models import User
from Intense.models import Comment,CommentReply,Reviews,Order,OrderDetails
from .serializers import CommentSerializer, CommentReplySerializer,ReviewsSerializer ,ProductReviewSerializer
from django.http.response import JsonResponse
from django.contrib.auth import get_user_model


class SerpyListProductAPIView(ListAPIView):
    queryset = Product.objects.all()
    serializer_class = SerpyProductSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['category', 'in_stock']


class ListProductView(ListAPIView):
    permission_classes = (ModelViewSetsPermission,)
    serializer_class = CreateProductSerializer
    filter_backends = [DjangoFilterBackend]
    search_fields = ("title",)
    ordering_fields = ("created",)
    filter_fields = ("title",)
    queryset = Product.objects.all()

    def update(self, request, *args, **kwargs):

        if User.objects.get(username="username") != self.get_object().seller:
            raise NotAcceptable(_("you don't own product"))
        return super(ListProductView, self).update(request, *args, **kwargs)



class CategoryListAPIView(ListAPIView):
    # permission_classes = [permissions.IsAuthenticated]
    serializer_class = CategoryListSerializer
    filter_backends = [DjangoFilterBackend]
    search_fields = ("title",)
    ordering_fields = ("created",)
    filter_fields = ("created",)
    # queryset = Category.objects.all()

    @time_calculator
    def time(self):
        return 0

    def get_queryset(self):
        queryset = Category.objects.all()
        self.time()
        return queryset


class CategoryAPIView(RetrieveAPIView):
    # permission_classes = [permissions.IsAuthenticated]
    serializer_class = CategoryListSerializer
    queryset = Category.objects.all()

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        data = {}
        # for k, v in serializer.data.items():
        #     data[k] = translator.translate(str(v), dest="ar").text

        return Response(data)

class CreateCategoryAPIView(CreateAPIView):
    #permission_classes = [auth.authenticate]
    serializer_class = CategoryListSerializer

    def create(self, request, *args, **kwargs):
        #user = request.user
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class DestroyCategoryAPIView(DestroyAPIView):
    #permission_classes = [auth.authenticate]
    serializer_class = CategoryListSerializer
    queryset = Product.objects.all()

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.is_deleted = True
        instance.save()
        return Response({"detail": "Category deleted"})



class ListProductAPIView(ListAPIView):
    serializer_class = ProductSerializer
    filter_backends = [DjangoFilterBackend]
    search_fields = ("title",)
    ordering_fields = ("created",)
    filter_fields = ("title",)
    queryset = Product.objects.all()

    @time_calculator
    def time(self):
        return 0

    # Cache requested url for each user for 2 hours
    @method_decorator(cache_page(60 * 60 * 2))
    @method_decorator(vary_on_cookie)
    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        self.time()
        return Response(serializer.data)


class ListUserProductAPIView(ListAPIView):
    serializer_class = ProductSerializer
    filter_backends = [DjangoFilterBackend]
    search_fields = (
        "title",
        "user__username",
    )
    ordering_fields = ("created",)
    filter_fields = ("title",)

    def get_queryset(self):
        user = self.request.user
        queryset = Product.objects.filter(user=user)
        return queryset


class CreateProductAPIView(CreateAPIView):
    #permission_classes = [permissions.IsAuthenticated]
    serializer_class = CreateProductSerializer

    def create(self, request, *args, **kwargs):
        user = request.user
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(seller=user)
        #push_notifications(user, request.data["title"], "you have add a new product")
        # if user.profile.phone_number:
        #     send_message(user.profile.phone_number, "Congratulations, you Created New Product")
        logger.info(
            "product ( "
            + str(serializer.data.get("title"))
            + " ) created"
            + " by ( "
            + str(user.username)
            + " )"
        )
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class DestroyProductAPIView(DestroyAPIView):
    #permission_classes = [IsOwnerAuth]
    serializer_class = ProductDetailSerializer
    queryset = Product.objects.all()

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.is_deleted = True
        instance.save()
        return Response({"detail": "Product deleted"})


class ProductViewsAPIView(ListAPIView):
    # permission_classes = [IsOwnerAuth]
    serializer_class = ProductViewsSerializer
    queryset = ProductViews.objects.all()


class ProductDetailView(APIView):
    def get(self, request, uuid):
        product = Product.objects.get(uuid=uuid)
        x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
        if x_forwarded_for:
            ip = x_forwarded_for.split(",")[0]
        else:
            ip = request.META.get("REMOTE_ADDR")

        if not ProductViews.objects.filter(product=product, ip=ip).exists():
            ProductViews.objects.create(product=product, ip=ip)

            product.views += 1
            product.save()
        serializer = ProductDetailSerializer(product, context={"request": request})

        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, pk):
        user = request.user
        product = get_object_or_404(Product, pk=pk)
        if product.user != user:
            raise PermissionDenied("this product don't belong to you.")

        serializer = ProductDetailSerializer(
            product, data=request.data, context={"request": request}
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


# class VariationListView(ListAPIView):
# 	model = Variation
# 	queryset = Variation.objects.all()

# 	def get_context_data(self, *args, **kwargs):
# 		context = super(VariationListView, self).get_context_data(*args, **kwargs)
# 		context["formset"] = VariationInventoryFormSet(queryset=self.get_queryset())
# 		return context

# 	def get_queryset(self, *args, **kwargs):
# 		product_pk = self.kwargs.get("pk")
# 		if product_pk:
# 			product = get_object_or_404(Product, pk=product_pk)
# 			queryset = Variation.objects.filter(product=product)
# 		return queryset

# 	def post(self, request, *args, **kwargs):
# 		formset = VariationInventoryFormSet(request.POST, request.FILES)
# 		if formset.is_valid():
# 			formset.save(commit=False)
# 			for form in formset:
# 				new_item = form.save(commit=False)
# 				#if new_item.title:
# 				product_pk = self.kwargs.get("pk")
# 				product = get_object_or_404(Product, pk=product_pk)
# 				new_item.product = product
# 				new_item.save()
				
# 			messages.success(request, "Your inventory and pricing has been updated.")
# 			return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view (["GET","POST"])
def group_product(request):
    #permission_classes = [permissions.IsAuthenticated]
    values = {'product_id' : '1', 'title': 'Group product Title','products_ids': ['1,2,3,4']}
    serializer_class = GroupProductSerializer
    product = GroupProduct.objects.filter(product_id = values['product_id']).last()
    if product is None:
        group_serializer = GroupProductSerializer (data= values)
        if(group_serializer.is_valid()):
            group_serializer.save()
            return Response (group_serializer.data, status=status.HTTP_201_CREATED)
        return Response (group_serializer.errors)

    else:
        product.products_ids.append(values['products_id'])
        product_val = product.__dict__
        serializer_value = GroupProductSerializer (product,data= product_val)
        if(serializer_value.is_valid()):
            serializer_value.save()
            return Response (serializer_value.data, status=status.HTTP_201_CREATED)
        return Response (serializer_value.errors)



class DestroyGroupProductAPIView(DestroyAPIView):
    #permission_classes = [IsOwnerAuth]
    serializer_class = GroupProductSerializer
    queryset = GroupProduct.objects.all()

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.is_deleted = True
        instance.save()
        return Response({"detail": "GroupProduct deleted"})


class GroupProductViewsAPIView(ListAPIView):
    # permission_classes = [IsOwnerAuth]
    serializer_class = GroupProductSerializer
    queryset = GroupProduct.objects.all()


class GroupProductDetailView(APIView):
    def get(self, request, uuid):
        group_product = GroupProduct.objects.get(uuid=uuid)
        x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
        if x_forwarded_for:
            ip = x_forwarded_for.split(",")[0]
        else:
            ip = request.META.get("REMOTE_ADDR")

        if not GroupProduct.objects.filter(group_product=group_product, ip=ip).exists():
            GroupProduct.objects.create(group_product=group_product, ip=ip)

            group_product.views += 1
            group_product.save()
        serializer = GroupProductSerializer(group_product, context={"request": request})

        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, pk):
        user = request.user
        product = get_object_or_404(Product, pk=pk)
        if product.user != user:
            raise PermissionDenied("this product don't belong to you.")

        serializer = GroupProductSerializer(
            product, data=request.data, context={"request": request}
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)



#------------Product comments and reviews

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
            return sonResponse(replyserializer.errors)

                
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