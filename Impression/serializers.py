from rest_framework import serializers
from Intense.models import ProductImpression

class ProductImpressionSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImpression
        fields = "__all__"


class userImpressionSerializer(serializers.ModelSerializer):
    verified_user_data = serializers.SerializerMethodField('verified_user_impression')
    non_verified_user_data = serializers.SerializerMethodField('non_verified_user_impression')

    class Meta:
        model = ProductImpression
        fields = ('verified_user_data','product_id','dates','non_verified_user_data')

    def verified_user_impression(self,obj):
        users=[]
        for val in obj.Users:
            if val is not -1:
                users.append(val)
        return users

    def non_verified_user_impression(self,obj):
        non_verified =[]
        for val in obj.non_verified_user:
            if val is not -1:
                non_verified.append(val)
        return non_verified

class ClickImpressionSerializer(serializers.ModelSerializer):
    click_impression = serializers.SerializerMethodField('product_click_impression')

    class Meta:
        model = ProductImpression
        fields = ('click_impression','product_id','dates')

    def product_click_impression(self,obj):
        return obj.click_count


class ViewImpressionSerializer(serializers.ModelSerializer):
    views_impression = serializers.SerializerMethodField('product_view_impression')

    class Meta:
        model = ProductImpression
        fields = ('views_impression','product_id','dates')

    def product_view_impression(self,obj):
        return obj.view_count

class CartImpressionSerializer(serializers.ModelSerializer):
    cart_impression = serializers.SerializerMethodField('product_cart_impression')

    class Meta:
        model = ProductImpression
        fields = ('cart_impression','product_id','dates')

    def product_cart_impression(self,obj):
        return obj.cart_count

class SalesImpressionSerializer(serializers.ModelSerializer):
    sales_impression = serializers.SerializerMethodField('product_sales_impression')

    class Meta:
        model = ProductImpression
        fields = ('sales_impression','product_id','dates')

    def product_sales_impression(self,obj):
        return obj.sales_count