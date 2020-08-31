from rest_framework import serializers

from django.contrib.auth.models import User
from Intense.models import Product,Order,OrderDetails,ProductPrice,Userz,BillingAddress,ProductPoint,ProductSpecification
from Intense.models import discount_product
from django.utils import timezone
from colour import Color

# Serializers define the API representation.
class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ('id','title','quantity')



class OrderSerializer(serializers.ModelSerializer):
    price_total = serializers.SerializerMethodField(method_name='get_price')
    point_total = serializers.SerializerMethodField(method_name='get_point')
    orders = serializers.SerializerMethodField(method_name='order_details')

    
    class Meta:
        model = Order
        #fields ='__all__'
        fields = ('id','date_created','order_status','delivery_status','user_id','non_verified_user_id','ip_address','checkout_status','price_total','point_total','ordered_date','orders')


    #This method is to calculate the total price
    def get_price(self,instance):
        sum_total = 0
        try:

            order_details = OrderDetails.objects.filter(order_id = instance.id,is_removed=False)
        except:
            order_details = None

        if order_details is not None:

            order_prices = order_details.values_list('product_id',flat = True)
            order_quantity = order_details.values_list('total_quantity',flat = True)
            sum_total= 0
            p_price = 0 
        
            for i in range(len(order_quantity)):
                try:
                    product_price = ProductPrice.objects.filter(product_id=order_prices[i]).last()
                except:
                    product_price = None
                try:

                    product_discount = discount_product.objects.filter(product_id=order_prices[i]).last()

                except:
                    product_discount = None
                

                if product_price is not None:
                    p_price = product_price.price

                else:
                    p_price = 0

               

          
                if product_discount is not None:
                    p_discount = product_discount.amount
                    start_date = product_discount.start_date
                    end_date = product_discount.end_date
                    current_date = timezone.now().date()


                    if (current_date >= start_date) and (current_date <= end_date):
                        total_discount = p_discount * order_quantity[i]
                        total_price = (p_price * order_quantity[i]) - total_discount
                        sum_total += total_price

                    else:

                        total_discount = 0
                        total_price = (p_price * order_quantity[i]) - total_discount
                        sum_total += total_price

                else:

                    
                    total_price = (p_price * order_quantity[i]) 
                    sum_total += total_price

        else:
            sum_total = 0

        float_total = format(sum_total, '0.2f')
        return float_total


    def get_point(self,instance):
        sum_total = 0 
        try:
            order_details = OrderDetails.objects.filter(order_id = instance.id,is_removed=False)

        except:
            order_details = None
        if order_details is not None:

            order_prices = order_details.values_list('product_id',flat = True)
            order_quantity = order_details.values_list('total_quantity',flat = True)
            sum_total= 0
            
            for i in range(len(order_quantity)):
                try:
                    product_point = ProductPoint.objects.filter(product_id=order_prices[i]).last()
                except:
                    product_point = None

                if product_point is not None:
                    p_point = product_point.point
                    start_date = product_point.start_date
                    end_date = product_point.end_date
                    current_date = timezone.now().date()
                    if (current_date >= start_date) and (current_date <= end_date):
                        total_point = p_point * order_quantity[i]
                        sum_total += total_point

                else:
                    sum_total = sum_total


        else:
            sum_total = 0
               

        float_total = format(sum_total, '0.2f')
        return float_total


    def order_details(self,instance):
        details = OrderDetails.objects.filter(order_id=instance.id,is_removed=False).values()
        list_result = [entry for entry in details]
        

        return list_result
            
            







class OrderDetailsSerializer(serializers.ModelSerializer):
    #price = serializers.SerializerMethodField(method_name='get_price')
    #points = serializers.SerializerMethodField(method_name='get_point')
    class Meta:
        model = OrderDetails
        fields = ('id','order_id','product_id','quantity','total_quantity','date_added','is_removed','unit_price','total_price','unit_point','total_point','product_name')
    
    #This method is to calculate the price of the individual items
    def get_price(self,instance):
        product_price = ProductPrice.objects.filter(product_id=instance.product_id).last()
        p_price = product_price.price
     

        total_price = p_price * instance.total_quantity
        float_total = format(total_price, '0.2f')
        return float_total

    def get_point(self,instance):
        product_point = ProductPoint.objects.filter(product_id=instance.product_id).last()
        p_point = product_point.point
        start_date = product_point.start_date
        end_date = product_point.end_date
        current_date = timezone.now().date()
        if (current_date >= start_date) and (current_date <= end_date):
            total_point = p_point * instance.total_quantity

        else:
            total_point = 0
     
        float_total = format(total_point, '0.2f')
        return float_total

  



class ProductPriceSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductPrice
        fields = ('id','product_id','price','date_added','currency_id')


class ProductPointSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductPoint
        fields = ('id','product_id','point','start_date','end_date') 
    



class BillingAddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = BillingAddress
        fields = ('id','user_id','address','date_created','date_updated','non_verified_user_id','ip_address')


class UserzSerializer(serializers.ModelSerializer):
    class Meta:
        model = Userz
        fields="__all__"


class ProductSpecificationSerializer(serializers.ModelSerializer):
    #hexcolor = serializers.SerializerMethodField(method_name='get_color')
    class Meta:
        model = ProductSpecification
        fields = ('id','product_id','color','size','unit','weight') 

    # def get_color(self,instance):
    #     product_color = ProductSpecification.objects.filter(id = instance.id).last()
    #     color = product_color.color
    #     colorhex = Color(color).hex
 
    #     return colorhex
