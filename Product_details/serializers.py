from rest_framework import serializers
from Intense.models import (ProductPoint,ProductPrice,ProductSpecification ,Product,Comment,CommentReply,
Reviews,discount_product,ProductImage,Cupons,ProductImpression,Warehouse,Shop,WarehouseInfo,ShopInfo,ProductBrand)
from django.contrib.auth.models import User
#from Cart.models import ProductPoint
from django.utils import timezone
from colour import Color
import requests
from django.urls import reverse,reverse_lazy
#from Intense.Integral_apis import ratings
import json

site_path = "http://127.0.0.1:8000/"
#site_path = "https://tango99.herokuapp.com/"
# site_path = "http://128.199.66.61:8080/"
#site_path = "https://tes.com.bd/"


# Serializers define the API representation.


class ProductPriceSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductPrice
        fields = "__all__"


class ProductPointSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductPoint
        fields = ('id','product_id','point','start_date','end_date') 


class ProductSpecificationSerializer(serializers.ModelSerializer):
    #hexcolor = serializers.SerializerMethodField(method_name='get_color')
    class Meta:
        model = ProductSpecification
        fields = ('id','product_id','color','size','weight','quantity') 



class ProductSpecificationSerializerz(serializers.ModelSerializer):
    #hexcolor = serializers.SerializerMethodField(method_name='get_color')
    product_title = serializers.SerializerMethodField(method_name='get_title')
    class Meta:
        model = ProductSpecification
        fields = ('id','product_id','color','size','weight','quantity','product_title') 



    def get_title(self,instance):

        title = ""

        try:

            product = Product.objects.get(id=instance.product_id)

        except:

            product = None

        if product:

            title = product.title

        return title




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
        fields = ('id','title','description','brand','quantity','key_features','old_price','new_price','unit','specification','ratings','reviews','question_answers','images','imagez')

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


            if product_discount.amount:
                p_discount = product_discount.amount
            else:
                p_discount = 0



            #p_discount = product_discount.amount
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

        arr =  {'colors':[],'sizes':[]}


        
        try:


            p_spec = ProductSpecification.objects.filter(product_id = instance.id)

        except:

            p_spec = None 


        if p_spec:

            print("duhbduhfbrfbrfhbgfbfhvbf")

            colors = list(p_spec.values_list('color',flat=True).distinct())
            sizes = list(p_spec.values_list('size',flat=True).distinct())
            # units = list(p_spec.values_list('unit',flat=True).distinct())
            if sizes == [None]:
                sizes= []


            if colors == [None]:
                colors = []

            arr =  {'colors':colors,'sizes':sizes}

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


# class WareHouseSerializer(serializers.ModelSerializer):

#     item_quantity = serializers.SerializerMethodField(method_name='get_quantity')
#     class Meta:
#         model = Warehouse
#         fields = ('id','warehouse_name','warehouse_location','item_quantity')


#     def get_




class WarehouseSerializer(serializers.ModelSerializer):
    products = serializers.SerializerMethodField(method_name='get_products')
    class Meta:
        model = Warehouse
        fields = ('id','warehouse_name','warehouse_location','products')


    def get_products(self,instance):

        product_data = []

        print("dhuklam")

        try:

            products = WarehouseInfo.objects.filter(warehouse_id=instance.id)

        except:

            products = None

        print("warehouse info")
        print(products)  


        if products:

            product_ids = list(products.values_list('product_id',flat=True).distinct())


            print("product ids")

            print(product_ids)

            if len(product_ids) > 0:

                print("dhuklam loop er bhitore")


                for i in range(len(product_ids)):

                    print("yeeeesssss")


                    try:

                        specific_product = Product.objects.get(id = product_ids[i])

                    except:

                        specific_product = None 

                    print(specific_product)


                    if specific_product:

                        product_id = specific_product.id
                        print("productid")
                        print(product_id)

                        product_title = specific_product.title
                        print(product_title)

                        #Finding out the product price 

                        try:

                            product_price = ProductPrice.objects.filter(product_id=product_id).last()
                        except:
                            product_price = None

                        if product_price is not None:
                            old_price = product_price.price
                            p_price = product_price.price
                            #unit_price = p_price
                        else:
                            old_price = 0
                            p_price = 0
                            #unit_price = p_price

                        #Fetching the product discount
                        try:
                            product_discount = discount_product.objects.filter(product_id=product_id).last()
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
                              
                                p_price = p_price - p_discount

                            else:
                                #total_discount=0
                                #total_price = (p_price * quantity) - total_discount
                                p_price = p_price
                        else:

                            p_price

                        print("price")
                        print(p_price)
                        print(old_price)

                        specifications = [] 


                        try:


                            spec_prods = WarehouseInfo.objects.filter(warehouse_id=instance.id,product_id=product_id)


                        except:

                            spec_prods = None

                        print(spec_prods)

                        if spec_prods:

                            #Fetch the specification ids

                            specs_ids = list(spec_prods.values_list('specification_id',flat=True))


                            spec_quantities = list(spec_prods.values_list('quantity',flat=True))

                            total_quantity = sum(spec_quantities)

                            print("-----")
                            print(specs_ids)
                            print("-----")
                            print(spec_quantities)
                            print(total_quantity)

                            


                            for j in range (len(specs_ids)):

                                print("second loop ey dhuklam")

                                try:

                                    specific_spec = ProductSpecification.objects.get(id=specs_ids[j])

                                except:

                                    specific_spec = None 




                                if specific_spec:

                                    color = specific_spec.color
                                    weight = specific_spec.weight
                                    size = specific_spec.size

                                    print("specssss")
                                    print(color)
                                    print(weight)
                                    print(size)


                                else:

                                    color = ""
                                    weight = ""
                                    size = ""


                                spec_data = {"color":color,"size":size,"weight":weight,"quantity":spec_quantities[j]}

                                specifications.append(spec_data)
                            print(specifications)


                        else:

                            total_quantity = 0

                            specifications = []



                        product_datas = {"product_id":product_id,"product_title":product_title,"product_price":p_price,"total_quantity":total_quantity,"specifications":specifications}
                        print(product_datas)

                    else:

                        product_datas = {}


                    product_data.append(product_datas)

                return product_data


            else:

                return product_data


        else:

            return product_data






      

class ShopSerializer(serializers.ModelSerializer):
    products = serializers.SerializerMethodField(method_name='get_products')
    class Meta:
        model = Shop
        fields = ('id','shop_name','shop_location','products')

    def get_products(self,instance):

        product_data = []

        print("dhuklam")

        try:

            products = ShopInfo.objects.filter(shop_id=instance.id)

        except:

            products = None

        print("warehouse info")
        print(products)  


        if products:

            product_ids = list(products.values_list('product_id',flat=True).distinct())


            print("product ids")

            print(product_ids)

            if len(product_ids) > 0:

                print("dhuklam loop er bhitore")


                for i in range(len(product_ids)):

                    print("yeeeesssss")


                    try:

                        specific_product = Product.objects.get(id = product_ids[i])

                    except:

                        specific_product = None 

                    print(specific_product)


                    if specific_product:

                        product_id = specific_product.id
                        print("productid")
                        print(product_id)

                        product_title = specific_product.title
                        print(product_title)

                        #Finding out the product price 

                        try:

                            product_price = ProductPrice.objects.filter(product_id=product_id).last()
                        except:
                            product_price = None

                        if product_price is not None:
                            old_price = product_price.price
                            p_price = product_price.price
                            #unit_price = p_price
                        else:
                            old_price = 0
                            p_price = 0
                            #unit_price = p_price

                        #Fetching the product discount
                        try:
                            product_discount = discount_product.objects.filter(product_id=product_id).last()
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
                              
                                p_price = p_price - p_discount

                            else:
                                #total_discount=0
                                #total_price = (p_price * quantity) - total_discount
                                p_price = p_price
                        else:

                            p_price

                        print("price")
                        print(p_price)
                        print(old_price)

                        specifications = [] 


                        try:


                            spec_prods = ShopInfo.objects.filter(shop_id=instance.id,product_id=product_id)


                        except:

                            spec_prods = None

                        

                        if spec_prods:

                            #Fetch the specification ids

                            specs_ids = list(spec_prods.values_list('specification_id',flat=True))


                            spec_quantities = list(spec_prods.values_list('quantity',flat=True))

                            total_quantity = sum(spec_quantities)

          

                            


                            for j in range (len(specs_ids)):

                                print("second loop ey dhuklam")

                                try:

                                    specific_spec = ProductSpecification.objects.get(id=specs_ids[j])

                                except:

                                    specific_spec = None 




                                if specific_spec:

                                    color = specific_spec.color
                                    weight = specific_spec.weight
                                    size = specific_spec.size

                                    print("specssss")
                                    print(color)
                                    print(weight)
                                    print(size)


                                else:

                                    color = ""
                                    weight = ""
                                    size = ""


                                spec_data = {"color":color,"size":size,"weight":weight,"quantity":spec_quantities[j]}

                                specifications.append(spec_data)
                            print(specifications)


                        else:

                            total_quantity = 0

                            specifications = []



                        product_datas = {"product_id":product_id,"product_title":product_title,"product_price":p_price,"total_quantity":total_quantity,"specifications":specifications}
                        print(product_datas)

                    else:

                        product_datas = {}


                    product_data.append(product_datas)

                return product_data


            else:

                return product_data


        else:

            return product_data


class WarehouseInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = WarehouseInfo
        fields = "__all__"
      

class ShopInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShopInfo
        fields = "__all__"
   
   
        


class NewWarehouseInfoSerializer(serializers.ModelSerializer):
    previous_quantity = serializers.SerializerMethodField(method_name='get_quantity')
    warehouse_name = serializers.SerializerMethodField(method_name='get_warehouse_name')
    class Meta:
        model = Warehouse
        fields = ('id','previous_quantity','warehouse_name')
    def get_quantity(self,instance):
        previous_quantity= instance.quantity
        return previous_quantity
    def get_warehouse_name (self, instance):
        wh_name = Warehouse.objects.filter(id=instance.warehouse_id)
        return wh_name[0].warehouse_name 
    



class AddBrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductBrand
        fields = "__all__"








     








