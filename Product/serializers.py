import json
import serpy
from rest_framework import serializers
#from user_profile.models import User
from Intense.models import Category, Product, ProductViews , Variation ,GroupProduct,Comment,CommentReply,Reviews,User
from drf_extra_fields.fields import Base64ImageField
from django.db.models import Avg
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model

#from django.contrib.auth.models import User

#from django_elasticsearch_dsl_drf.serializers import DocumentSerializer
# from .documents import ProductDocument
# from ecommerce.serializers import LightSerializer, LightDictSerializer


class CategoryListSerializer(serializers.ModelSerializer):
    # lft = serializers.SlugRelatedField(slug_field='lft', read_only=True)
    class Meta:
        model = Category
        fields = '__all__'


class ProductSerializer(serializers.ModelSerializer):
    #seller = serializers.SlugRelatedField(slug_field="username", queryset=User.objects)
    category = serializers.SerializerMethodField()

    def get_category(self, obj):
        return obj.category.title

    class Meta:
        model = Product
        fields = '__all__'


class SerpyProductSerializer(serpy.Serializer):
    seller = serpy.StrField()
    category = serpy.StrField()
    title = serpy.StrField()
    price = serpy.FloatField()
    image = serpy.StrField()
    description = serpy.StrField()
    quantity = serpy.IntField()
    views = serpy.IntField()


class ProductMiniSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ["title"]

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data = serializers.ModelSerializer.to_representation(self, instance)
        return data


class CreateProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'
        # read_only_fields = ('id', 'seller', 'category', 'title', 'price', 'image', 'description', 'quantity', 'views',)


class ProductDetailSerializer(serializers.ModelSerializer):
    #seller = serializers.SlugRelatedField(slug_field="username", queryset=User.objects)
    category = serializers.SerializerMethodField()
    image = Base64ImageField()

    def get_category(self, obj):
        return obj.category.name

    class Meta:
        model = Product
        fields ='__all__'


class ProductViewsSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductViews
        fields = '__all__'



class VariationSerializer(serializers.ModelSerializer):
	class Meta:
		model = Variation
		fields = '__all__'



class GroupProductSerializer(serializers.ModelSerializer):
	product_set = ProductSerializer(many=True)
	class Meta:
		model = GroupProduct
		fields = '__all__'



# class ProductDocumentSerializer(DocumentSerializer):
#     seller = serializers.SlugRelatedField(slug_field="username", queryset=User.objects)
#     category = serializers.SerializerMethodField()

#     def get_category(self, obj):
#         return obj.category.name

#     class Meta(object):
#         # model = Product
#         document = ProductDocument
#         exclude = "modified"


#------------Comment Serializers---------------
User = get_user_model()
class CommentSerializer(serializers.ModelSerializer):
    replies = serializers.SerializerMethodField(method_name='get_replies')
    comment_name = serializers.SerializerMethodField(method_name='get_name')
    class Meta:
        model = Comment
        fields = ('id','comment','date_created','product_id','user_id','non_verified_user_id','replies','comment_name')

    def get_replies(self,instance):
        replys = CommentReply.objects.filter(comment_id=instance.id).values()
        list_result = [entry for entry in replys] 
    
        return list_result

    def get_name(self,instance):
            user_id = instance.user_id
            non_verified_user_id = instance.non_verified_user_id
            comment_name=""
            
    
            if user_id is not None:
                user_id = int(user_id)
                non_verified_user_id =0

            else:
                non_verified_user_id = non_verified_user_id
                user_id = 0

            

            if non_verified_user_id == 0:


                try:


                    name = User.objects.filter(id=user_id).last()
                except:
                    name = None
                if name is not None:
                    comment_name = name.username
                    return comment_name
                else:
                    
                    return comment_name

            else:

                comment_name = "Anonymous"
                return comment_name



class CommentReplySerializer(serializers.ModelSerializer):
    class Meta:
        model = CommentReply
        fields = ('id','comment_id','reply','date_created','user_id','non_verified_user_id','name')


#------------Review Serializers--------------------
class ReviewsSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField(method_name='get_name')
    class Meta:
        model = Reviews
        fields = ('id','product_id','user_id','non_verified_user_id','name','content','image','rating','date_created')

    def get_name(self,instance):
            user_id = instance.user_id
            non_verified_user_id = instance.non_verified_user_id
            comment_name=""
            
    
            if user_id is not None:
                user_id = int(user_id)
                non_verified_user_id =0

            else:
                non_verified_user_id = non_verified_user_id
                user_id = 0

            

            if non_verified_user_id == 0:


                try:


                    name = User.objects.filter(id=user_id).last()
                except:
                    name = None
                if name is not None:
                    comment_name = name.username
                    return comment_name
                else:
                    
                    return comment_name

            else:

                comment_name = "Anonymous"
                return comment_name




class ProductReviewSerializer(serializers.ModelSerializer):
    total_no_of_ratings = serializers.SerializerMethodField(method_name='total_ratings')
    total_no_of_reviews = serializers.SerializerMethodField(method_name='total_reviews')
    average_ratings = serializers.SerializerMethodField(method_name='average_rating')
    each_ratings = serializers.SerializerMethodField(method_name='each_rating')
    class Meta:
        model = Reviews
        fields = ('product_id','total_no_of_ratings','total_no_of_reviews','average_ratings','each_ratings')

    def total_ratings(self,instance):
        try:

            product = Reviews.objects.filter(product_id=instance.product_id).count()

        except:

            product = None

        return int(product)

    def total_reviews(self,instance):
        try:

            product = Reviews.objects.filter(product_id=instance.product_id).count()

        except:

            product = None

        return int(product)


    def average_rating(self,instance):

        

        try:

            product = Reviews.objects.filter(product_id=instance.product_id)
            product_count = Reviews.objects.filter(product_id=instance.product_id).count()
            review_ids = product.values_list('rating' , flat = True)
            total_count = 0

            for i in range(len(review_ids)):
                total_count += review_ids[i]

            average = total_count/product_count

            num1 = int(average)
            #print(num1)
            num2 = average%1
            if num2>0.5:
                num2=1
            elif num2 == 0.5:
                num2=0.5
            else:
                num2=0

            #print(num2)

            num = num1 + num2
                


        except:

            product = None

        return num

    def each_rating(self,instance):

        sum_one = 0
        sum_two = 0
        sum_three = 0
        sum_four = 0
        sum_five =0 

        try:
            product = Reviews.objects.filter(product_id=instance.product_id)
            review_ids = product.values_list('rating' , flat = True)

            for i in range(len(review_ids)):
                if review_ids[i] == 1:
                    sum_one += 1

                elif review_ids[i] == 2:
                    sum_two += 1


                elif review_ids[i] == 3:
                    sum_three += 1


                elif review_ids[i] == 4:
                    sum_four += 1

                else:
                    sum_five += 1



            nums = [{"rating":1,"count":sum_one},{"rating":2,"count":sum_two},{"rating":3,"count":sum_three},{"rating":4,"count":sum_four},{"rating":5,"count":sum_five}]




        except:
            product = None

        return nums


