from rest_framework import serializers
from Intense.models import ProductPoint,ProductPrice,ProductSpecification ,Product,Comment,CommentReply,Reviews,discount_product,ProductImage,Cupons,ProductImpression
from django.contrib.auth.models import User
#from Cart.models import ProductPoint
from django.utils import timezone
from colour import Color
import requests
from django.urls import reverse,reverse_lazy
#from Intense.Integral_apis import ratings
import json

#site_path = "http://127.0.0.1:8000/"
site_path = "https://tango99.herokuapp.com/"


# Serializers define the API representation.


class ProductPriceSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductPrice
        fields = ('id','product_id','price','date_added','currency_id')


class ProductPointSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductPoint
        fields = ('id','product_id','point','start_date','end_date') 


class ProductSpecificationSerializer(serializers.ModelSerializer):
    #hexcolor = serializers.SerializerMethodField(method_name='get_color')
    class Meta:
        model = ProductSpecification
        fields = ('id','product_id','color','size','unit','weight','quantity') 


class ProductDetailSerializer(serializers.ModelSerializer):
    old_price = serializers.SerializerMethodField(method_name='get_price')
    new_price = serializers.SerializerMethodField(method_name='get_discounted_price')
    specification = serializers.SerializerMethodField(method_name='get_specification')
    quantity = serializers.SerializerMethodField(method_name='get_quantity')

    #availability = serializers.SerializerMethodField(method_name='available')
    ratings = serializers.SerializerMethodField(method_name='get_ratings')
    reviews = serializers.SerializerMethodField(method_name='get_reviews')
    images = serializers.SerializerMethodField(method_name='get_images')
    imagez = serializers.SerializerMethodField(method_name='get_imagez')
    question_answers = serializers.SerializerMethodField(method_name='get_comments')
    class Meta:
        model = Product
        fields = ('id','title','description','quantity','key_features','old_price','specification','new_price','ratings','reviews','question_answers','images','imagez')

    def get_price(self,instance):
        p_price = 0

        try:
            product_price = ProductPrice.objects.filter(product_id = instance.id).last()
        except:
            product_price = None

        if product_price is not None:
            p_price = product_price.price

        else:
            p_price = 0

        float_total = format(p_price, '0.2f')
        return float_total


    def get_discounted_price(self,instance):
        p_price = 0
        p_discount = 0
        discounted_price =0


        try:
            product_price = ProductPrice.objects.filter(product_id=instance.id).last()
        except:
            product_price = None
        try:

            product_discount = discount_product.objects.filter(product_id=instance.id).last()

        except:
            product_discount = None
        

        if product_price is not None:
            p_price = product_price.price

        else:
            p_price = 0


        if product_discount is not None:


            p_discount = product_discount.amount
            current_date = timezone.now().date()
            if product_discount.start_date:
                start_date = product_discount.start_date
            else:
                start_date = current_date

            if product_discount.end_date:
                end_date = product_discount.end_date

            else:
                end_date = current_date
            

            if(current_date >= start_date) and (current_date <= end_date):
                discounted_price = p_price - p_discount

            else:
                discounted_price = p_price

        else:
            discounted_price = p_price


        float_total = format(discounted_price, '0.2f')
        return float_total


    def get_ratings(self,instance):


        product_id = instance.id
        #site_path = "https://tango99.herokuapp.com/"

        url = site_path+ "product/ratings/"+str(product_id)+"/"
        values = requests.get(url).json()
        return values


    def get_reviews(self,instance):


        product_id = instance.id
        #site_path = "https://tango99.herokuapp.com/"

        url = site_path+ "product/reviews_product/"+str(product_id)+"/"
        values = requests.get(url).json()
        return values

    def get_comments(self,instance):


        product_id = instance.id
        #site_path = "https://tango99.herokuapp.com/"

        url = site_path+ "product/comments_product/"+str(product_id)+"/"
        values = requests.get(url).json()
        return values


    # def get_specifications(self,instance):


    #     product_id = instance.id
    #     #site_path = "https://tango99.herokuapp.com/"

    #     url = site_path+ "productdetails/showspec/"+str(product_id)+"/"
    #     values = requests.get(url).json()
    #     return values

    def get_specification(self,instance):

        arr =  {'colors':[],'sizes':[],'units':[]}


        
        try:


            p_spec = ProductSpecification.objects.filter(product_id = instance.id)

        except:

            p_spec = None 


        if p_spec is not None:

            colors = list(p_spec.values_list('color',flat=True).distinct())
            sizes = list(p_spec.values_list('size',flat=True).distinct())
            units = list(p_spec.values_list('unit',flat=True).distinct())

            arr =  {'colors':colors,'sizes':sizes,'units':units}

            return arr

        else:

            return arr


    def get_quantity(self,instance):

        #arr =  {'colors':[],'sizes':[],'units':[]}

        total_sum = 0


        
        try:


            p_spec = ProductSpecification.objects.filter(product_id = instance.id)

        except:

            p_spec = None 


        if p_spec is not None:

            quantities = list(p_spec.values_list('quantity',flat=True))

            #total_sum = 0
            for i in range(len(quantities)):

                total_sum = total_sum + quantities[i]



            

            return total_sum

        else:

            return total_sum




    def get_images(self,instance):

        images=[]


        try:

            product_images = ProductImage.objects.filter(product_id = instance.id)

        except:
            product_images = None

        if product_images is not None:
            images = list(product_images.values_list('image_url' , flat = True))
            # images=[] 
            # for i in range(len(image_ids)):
            #     images += product_images.image


        else:
            images=[]

        return images


    def get_imagez(self,instance):
        replys = ProductImage.objects.filter(product_id=instance.id).values()
        list_result = [entry for entry in replys] 
    
        return list_result
# ------------------------- Product Cupon ---------------------------------

class CupponSerializer(serializers.ModelSerializer):
  
    class Meta:
        model = Cupons
        fields = "__all__"


# --------------------- Product Discount ---------------------

class ProductDiscountSerializer(serializers.ModelSerializer):
    class Meta:
        model = discount_product
        fields = "__all__"
        #fields=("name", "email")



class ProductImpressionSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImpression
        fields = "__all__"
        #fields=("name", "email")






   
   
        



    










     








