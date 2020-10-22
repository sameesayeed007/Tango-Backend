from django.shortcuts import render
from django.http import HttpResponse
from django.http.response import JsonResponse
from rest_framework.parsers import JSONParser 
from rest_framework import status
import datetime
 
from Intense.models import (Product,Order,OrderDetails,ProductPrice,Userz,BillingAddress,ProductPoint,ProductSpecification,
user_relation,Cupons,Comment,CommentReply,Reviews,discount_product,Warehouse,Shop,WarehouseInfo,ShopInfo,WarehouseInfo,inventory_report)
from Product_details.serializers import ProductPriceSerializer,ProductPointSerializer,ProductSpecificationSerializer,ProductSpecificationSerializerz,ProductDetailSerializer,CupponSerializer,ProductDiscountSerializer,WarehouseSerializer,ShopSerializer,WarehouseInfoSerializer,ShopInfoSerializer
from rest_framework.decorators import api_view 
from django.views.decorators.csrf import csrf_exempt
from datetime import datetime
from datetime import timedelta  
from django.utils import timezone
import requests
from django.urls import reverse,reverse_lazy
from django.http import HttpResponseRedirect
from django.conf import settings
from colour import Color
from rest_framework.response import Response


@api_view(['POST',])
def color_size(request,product_id):

    try:

        product = Product.objects.get(id = product_id)


    except:

        product = None 


    if product:

        product_spec = ProductSpecification.objects.filter(product_id=product_id)&ProductSpecification.objects.filter(quantity__gte=1)
            

        product_colors = list(product_spec.values_list('color',flat=True).distinct()) 

        return JsonResponse({'success':True , 'message':'The colors are shown','colors':product_colors})



    else:

        product_colors = []

        return JsonResponse({'success':False , 'message':'The colors are not shown','colors':product_colors})



@api_view(['POST',])
def available_sizes(request,product_id):

    color = request.data.get("color")

    try:

        product = Product.objects.get(id = product_id)


    except:

        product = None 


    if product:

        product_spec = ProductSpecification.objects.filter(product_id=product_id)&ProductSpecification.objects.filter(color=color)&ProductSpecification.objects.filter(quantity__gte=1)
            

        product_sizes = list(product_spec.values_list('size',flat=True).distinct())

        product_quantities =  list(product_spec.values_list('quantity',flat=True))

        dic = {}

        for i in range (len(product_sizes)):

            item = {product_sizes[i]:product_quantities[i]}

            dic.update(item)



        return JsonResponse({'success':True , 'message':'The colors are shown','sizes':product_sizes,'quantities':dic})



    else:

        product_sizes = []

        return JsonResponse({'success':False , 'message':'The colors are not shown','sizes':product_sizes})








@api_view(['POST',])
def add_points(request):

    if request.method == 'POST':
        pointserializer = ProductPointSerializer(data=request.data)
        if pointserializer.is_valid():
            pointserializer.save()
            return JsonResponse(pointserializer.data, status=status.HTTP_201_CREATED)
        return JsonResponse(pointserializer.errors)


#This updates the product points
@api_view(['POST',])
def update_points(request,product_id):

    try:
        product = ProductPoint.objects.filter(product_id=product_id).last()

        if request.method == 'POST':
            pointserializer = ProductPointSerializer(product,data=request.data)
            if pointserializer.is_valid():
                pointserializer.save()
                return JsonResponse(pointserializer.data, status=status.HTTP_201_CREATED)
            return JsonResponse(pointserializer.errors)

    except ProductPoint.DoesNotExist:
        return JsonResponse({'message': 'This product does not exist'}, status=status.HTTP_404_NOT_FOUND)




#This updates the product points
@api_view(['POST',])
def delete_points(request,product_id):

    try:
        product = ProductPoint.objects.filter(product_id=product_id)

        if request.method == 'POST':
            product.delete()


            return JsonResponse({'message': 'The product points have been deleted'})

    except ProductPoint.DoesNotExist:
        return JsonResponse({'message': 'This product does not exist'}, status=status.HTTP_404_NOT_FOUND)



#This adds the current product price
@api_view(['POST',])
def add_price(request):

    if request.method == 'POST':
        pointserializer = ProductPriceSerializer(data=request.data)
        if pointserializer.is_valid():
            pointserializer.save()
            return JsonResponse(pointserializer.data, status=status.HTTP_201_CREATED)
        return JsonResponse(pointserializer.errors)


#This updates the current product price
@api_view(['POST',])
def update_price(request,product_id):

    try:
        product = ProductPrice.objects.filter(product_id=product_id).last()

        if request.method == 'POST':
            pointserializer = ProductPriceSerializer(product,data=request.data)
            if pointserializer.is_valid():
                pointserializer.save()
                return JsonResponse(pointserializer.data, status=status.HTTP_201_CREATED)
            return JsonResponse(pointserializer.errors)

    except ProductPrice.DoesNotExist:
        return JsonResponse({'message': 'This product does not exist'}, status=status.HTTP_404_NOT_FOUND)




#This updates the product points
@api_view(['POST',])
def delete_price(request,product_id):

    try:
        product = ProductPrice.objects.filter(product_id=product_id)

        if request.method == 'POST':
            product.delete()


            return JsonResponse({'message': 'The product prices have been deleted'})

    except ProductPoint.DoesNotExist:
        return JsonResponse({'message': 'This product does not exist'}, status=status.HTTP_404_NOT_FOUND)


#This adds product points 
@api_view(['POST',])
def add_specification(request):

    if request.method == 'POST':
        pointserializer = ProductSpecificationSerializer(data=request.data)

        if pointserializer.is_valid():
            pointserializer.save()
            return JsonResponse({'success': True,'message': 'Data is shown below','data':pointserializer.data}, status=status.HTTP_201_CREATED)
        else:
            return JsonResponse({'success': False,'message': 'Data could not be inserted', 'data':{}})



#This updates the latest product specification
@api_view(['POST',])
def update_specification(request,product_id):


    try:
        product = ProductSpecification.objects.filter(product_id=product_id).last()

        if request.method == 'POST':
            pointserializer = ProductSpecificationSerializer(product,data=request.data)
            if pointserializer.is_valid():
                pointserializer.save()
                return JsonResponse(pointserializer.data, status=status.HTTP_201_CREATED)
            return Response (pointserializer.errors)

    except ProductPoint.DoesNotExist:
        return JsonResponse({'message': 'This product does not exist'}, status=status.HTTP_404_NOT_FOUND)




#This deletes the product specification
@api_view(['POST',])
def delete_specification(request,product_id):

    try:
        product = ProductSpecification.objects.filter(product_id=product_id)

        if request.method == 'POST':
            product.delete()


            return JsonResponse({'message': 'The product specification have been deleted'})

    except ProductPoint.DoesNotExist:
        return JsonResponse({'message': 'This product does not exist'}, status=status.HTTP_404_NOT_FOUND)


@api_view(['GET',])
def show_specification(request,product_id):


    try:
        title = Product.objects.get(id=product_id)
    except:
        title = None
    if title:
        product_title = title.title
    else:
        product_title = ''



    try:

        product = ProductSpecification.objects.filter(product_id=product_id)

    except:

        product = None

    if product:

        productserializer = ProductSpecificationSerializerz(product,many=True)
        data = productserializer.data

    else:

        data = {}

    return JsonResponse({
    'success': True,
    'message': 'Data is shown below',
    'product_title': product_title,
    'data': data

    })


        


    


@api_view(['POST',])
def add_spec(request,product_id):

    spec = ProductSpecification.objects.create(product_id=product_id)

    if request.method == 'POST':
        pointserializer = ProductSpecificationSerializer(spec,data=request.data)

        if pointserializer.is_valid():
            pointserializer.save()
            return JsonResponse({'success': True,'message': 'Data is shown below','data':pointserializer.data}, status=status.HTTP_201_CREATED)
        else:
            return JsonResponse({'success': False,'message': 'Data could not be inserted', 'data':{}})



@api_view(['POST',])
def edit_spec(request,specification_id):


    try:

        spec = ProductSpecification.objects.get(id=specification_id)

    except:
        spec = None 

    if spec:
        pointserializer = ProductSpecificationSerializer(spec,data=request.data)

        if pointserializer.is_valid():
            pointserializer.save()
            return JsonResponse(pointserializer.data, status=status.HTTP_201_CREATED)
        return Response (pointserializer.errors)



@api_view(['POST',])
def delete_spec(request,specification_id):


    try:

        spec = ProductSpecification.objects.get(id=specification_id)

    except:
        spec = None 

    if spec:
        spec.delete()
        return JsonResponse({'success':True,'message': 'The product specification have been deleted'})
    else:
        return JsonResponse({'success':False,'message': 'The product specification could not be deleted'})


@api_view(['GET',])
def show(request,product_id):

    #url = reverse('product_price_point_specification:showspec',args=[product_id])
    #data= requests.get(url)
    #url= reverse('product_price_point_specification:showspec',args=[product_id])
    #main = str(settings.BASE_DIR) + url
    #print(main)
    #data = requests.get(main)
    url=request.build_absolute_uri(reverse('product_price_point_specification:showspec',args=[product_id]))
    #print("------")
    #print(url)
    data= requests.get(url)
    return HttpResponse(data)                                                                                                                                                               
    

#This changes the comments,replies,reviews and order tables
@api_view(['POST',])
def transfer(request,user_id):
    # Here userid provided is the newly verified userid 
    try:
    
        existing_user = user_relation.objects.filter(verified_user_id=user_id).last()
        print(existing_user)

    except:
        existing_user = None

    if existing_user is not None:
        #Change the ids in the certain table

        # print(type(existing_user.verified_user_id))
        # print(existing_user.non_verified_user_id)
        user_id = existing_user.verified_user_id
        non_verified_user_id = existing_user.non_verified_user_id
    
        
        #Update all the order tables

        orders = Order.objects.filter(non_verified_user_id = non_verified_user_id).update(user_id=user_id,non_verified_user_id=None)
        
        #Update the Billing address

        billing_address = BillingAddress.objects.filter(non_verified_user_id=non_verified_user_id).update(user_id=user_id,non_verified_user_id=None)

        #Update the comment,reply and review tables

        comments = Comment.objects.filter(non_verified_user_id=non_verified_user_id).update(user_id=user_id,non_verified_user_id=None)
        reply = CommentReply.objects.filter(non_verified_user_id=non_verified_user_id).update(user_id=user_id,non_verified_user_id=None)
        reviews = Reviews.objects.filter(non_verified_user_id=non_verified_user_id).update(user_id=user_id,non_verified_user_id=None)
         
        return JsonResponse({'message': 'The user does exist'})
            
    else:
        return JsonResponse({'message': 'The user does not exist'})



@api_view(['GET',])
def product_detail(request,product_id):

    try:
        product = Product.objects.filter(id=product_id).last()

    except:
        product = None

    if product is not None:

        product_serializer = ProductDetailSerializer(product,many=False)
        return JsonResponse({'success':True,'message':'The data is shown below','data':product_serializer.data},safe=False)
        

    else:
        return JsonResponse({'success':False,'message':'This product does not exist','data':''}, status=status.HTTP_404_NOT_FOUND)
        




# --------------------------------- Product Cupon -------------------------------

@api_view(["GET","POST"])
def insert_cupon(request):
    '''
    This is for inserting cupon code into the databse. Admin will set the cupon code and it will apear to the users while buying a product.
    Calling http://127.0.0.1:8000/cupons/create_cupon/ will cause to invoke this Api. This Api just have Post response.

    Post Response:
        cupon_code : This is a character field. This will be cupon named after the inserting name value.
        amount : This will be the amount which will be deducted from the user payable balance.
        start_from: This is DateField. It will be created automatically upon the creation of a cupon.
        valid_to: This is another DateField. While creating a cupon admin will set the date.
        is_active : This is a BooleanField. This will indicate wheather the cupon is active or not. Using this data, cupon can be deactivated before ending
                    the validation time. 

    '''
    if(request.method == "POST"):
        serializers = CupponSerializer (data= request.data)
        if(serializers.is_valid()):
            serializers.save()
            return Response (serializers.data, status=status.HTTP_201_CREATED)
        return Response (serializers.errors)

@api_view(["GET","POST"])
def get_all_cupons(request):
    '''
    This is for getting all the cupons. Calling http://127.0.0.1:8000/cupons/all_cupon/ will cause to invoke this Api. 
    The Get Response will return following structured datas.

    Get Response:
        [
            {
                "id": 2,
                "cupon_code": "30% Off",
                "amount": 50.0,
                "start_from": "2020-08-27",
                "valid_to": "2020-09-30",
                "is_active": false
            },
            {
                "id": 3,
                "cupon_code": "25 Taka Off",
                "amount": 25.0,
                "start_from": "2020-08-27",
                "valid_to": "2020-10-27",
                "is_active": false
            }
        ]
    '''
    if(request.method == "GET"):
        queryset = Cupons.objects.all()
        serializers = CupponSerializer (queryset,many = True)
        return Response (serializers.data)

@api_view(["GET","POST"])
def update_specific_cupons(request,cupon_id):
    '''
    This is for updating a particular cupon. Calling http://127.0.0.1:8000/cupons/update_cupon/4/ will cause to invoke this Api.
    While calling this Api, as parameters cupon id must need to be sent.

    After updating expected Post Response:
        {
            "id": 4,
            "cupon_code": "25 Taka Off",
            "amount": 25.0,
            "start_from": "2020-08-27",
            "valid_to": "2020-10-27",
            "is_active": true
        }
    '''

    try: 
        cupon = Cupons.objects.get(pk = cupon_id)
    except :
        return Response({'Message': 'Check wheather requested data exists or not'})

    if(request.method == "GET"):
        cupon_serializer = CupponSerializer(cupon, many=False)
        return Response (cupon_serializer.data)

    elif(request.method == "POST"):
        Cupon_serializers = CupponSerializer( cupon, data= request.data)
        if(Cupon_serializers.is_valid()):
            Cupon_serializers.save()
            return Response (Cupon_serializers.data, status=status.HTTP_201_CREATED)
        return Response (Cupon_serializers.errors)

@api_view(["GET","POST"])
def delete_specific_cupons(request,cupon_id):
    '''
    This is for deleting a particular cupon value. Calling 127.0.0.1:8000/cupons/delete_cupon/4/ will cause to invoke this Api.
    After performing delete operation successfully this api will provide following response.

    Successful Post Response:
        [
            "Cupon has been deleted successfully"
        ]
    Unsuccessful Post Response:
        {
            "Message": "Some internal problem occurs while deleting the value"
        }
    '''

    try: 
        cupon = Cupons.objects.get(pk = cupon_id)
    except :
        return Response({'Message': 'Some internal problem occurs while deleting the value'})

    if(request.method == "POST"):
        cupon.delete()
        return Response({'Cupon has been deleted successfully'})

    
    # --------------------------- Product Discount -----------------------

@api_view (["GET","POST"])
def get_all_discount_value(request):
    '''
    This api is for getting all the discount related information. Calling http://127.0.0.1:8000/discount/all_discount/ will invoke
    this API. This API just have get response.
    
    GET Response:
        discount_type (This will be a Chartype data. This will return the type of discount like Flat, Flash, Wholesale etc.)
        amount (This will return the amount which will be apply where discount is applicable.)
        start_date (This is the discount start date. From this date discount will be started.)
        end_date  (This is discount end date. On this date, discount will be end.)
        max_amount (Sometimes, admin can restrict the highest level of amount for discount. This value represents that highest amount value.) 
    '''
   
    if(request.method == "GET"):
        queryset = discount_product.objects.all()
        discount_serializers = ProductDiscountSerializer (queryset,many = True)
        return Response (discount_serializers.data)

@api_view (["GET","POST"])
def insert_specific_discount_value(request):
    '''
    This Api is for just inserting the particular discount value corresponding to a product. It has just Post response. Calling 
    http://127.0.0.1:8000/discount/insert_specific/ cause to invoke this api.

    POST Response:
        Following values field this api expects while performing post response.
        Discount (It will be type of discount, simply a name.)
        amount (This will be a float value. This amount value will be used to calculate the discount value)
        start_date ( This is the date from when the discount will be started.)
        end_date (On this date, the discount will end)
        max_amount (Admin can set the highest amount of discount. Something like 30% discount upto 50 taka. Here, max amount 50 taka.)
        product_id or group_product_id ( product_id or group_product_id, on which the discount will be performed must need to provide.)
    '''
    if(request.method == "POST"):
        discount_serializers = ProductDiscountSerializer (data= request.data)
        if(discount_serializers.is_valid()):
            discount_serializers.save()
            return Response (discount_serializers.data, status=status.HTTP_201_CREATED)
        return Response (discount_serializers.errors)


@api_view (["GET","POST"])
def get_update_specific_value(request,product_id):
    '''
    This Api is for getting a particular discount value. This will need to update a particular information. Admin may change the end date of discount or 
    may increase the amount value. Calling http://127.0.0.1:8000/discount/specific_value/3/ will cause to invoke this API. This Api has both 
    Post and Get response.
    prams : Product_id
    Get Response:
        discount_type (This will be a Chartype data. This will return the type of discount like Flat, Flash, Wholesale etc.)
        amount (This will return the amount which will be apply where discount is applicable.)
        start_date (This is the discount start date. From this date discount will be started.)
        end_date  (This is discount end date. On this date, discount will be end.)
        max_amount (Sometimes, admin can restrict the highest level of amount for discount. This value represents that highest amount value.) 
    
    POST Response:
        Following values field this api expects while performing post response.
        Discount (It will be type of discount, simply a name.)
        amount (This will be a float value. This amount value will be used to calculate the discount value)
        start_date ( This is the date from when the discount will be started.)
        end_date (On this date, the discount will end)
        max_amount (Admin can set the highest amount of discount. Something like 30% discount upto 50 taka. Here, max amount 50 taka.)
        product_id or group_product_id ( product_id or group_product_id, on which the discount will be performed must need to provide.)


    '''
    # Demo Values
    try: 
        specific_values = discount_product.objects.get(product_id = product_id) 
    except :
        return Response({'message': 'This value does not exist'})

    if(request.method == "GET"):
        discount_serializer_value = ProductDiscountSerializer(specific_values, many=False)
        return Response (discount_serializer_value.data)

    elif(request.method == "POST"):
        try:
            discount_serializer_value = ProductDiscountSerializer (specific_values,data= request.data)
            if(discount_serializer_value.is_valid()):
                discount_serializer_value.save()
                return Response (discount_serializer_value.data, status=status.HTTP_201_CREATED)
            return Response (discount_serializer_value.errors)
        except:
            return Response({'message': 'Discount value could not be updated'})

@api_view(['POST','GET'])
def delete_discount_value(request,product_id):
    '''
    This Api is for deleting a particular discount value. Based on the provided product_id or group_product_id this will delet the discount value.
    Calling http://127.0.0.1:8000/discount/discount_delete/4 will cause to invoke this api. After deleting the value, in response this api will 
    send a successful message. If it can not delete then it will provide an error message.

    prams : product_id
    ''' 
    
    try: 
        specific_values = discount_product.objects.get(product_id = product_id) 
    except :
        return Response({'message': 'There is no value to delete'})
    
    if request.method == 'POST':
        specific_values.delete()
        return Response({'message': ' Value is successfully  deleted'}, status=status.HTTP_204_NO_CONTENT)




@api_view(["GET", "POST"])
def get_product_lists(request, order_id):

    if(request.method == "GET"):

        try:
            ware_house = []
            shops = []
            order_info = OrderDetails.objects.filter(order_id=order_id)
            print(order_info)

            for orders in order_info:
                all_specification = ProductSpecification.objects.get(
                    product_id=orders.product_id, size=orders.product_size, color=orders.product_color)
                print(all_specification)
                ware_house_info = Warehouse.objects.filter(
                    specification_id=all_specification.id)
                if ware_house_info:
                    ware_house_data = WareHouseSerializer(
                        ware_house_info, many=True)
                    ware_house.append(ware_house_data.data)
                shop_info = Shop.objects.filter(
                    specification_id=all_specification.id)
                if shop_info.exists():
                    shop_data = ShopSerializer(shop_info, many=True)
                    shops.append(shop_data.data)
        except:
            return Response({'Message': 'Check whether requested data exists or not'})

        return Response({
            "success": True,
            "Message": "Data is shown bellow",
            "warehouse": ware_house,
            "Shop": shops
        })




@api_view(["GET",])
def get_inventory_lists(request, order_details_id):


    try:

        product = OrderDetails.objects.get(id=order_details_id)

    except:

        product = None 


   


    if product:


        product_id = product.product_id
        product_size = product.product_size
        product_color = product.product_color



        try:

            spec = ProductSpecification.objects.get(
                    product_id=product_id, size=product_size, color=product_color) 


        except:

            spec = None 


        


        if spec:

            specification_id = spec.id 


            try:

                warehouses = Warehouse.objects.filter(specification_id=specification_id)

            except:

                warehouses = None





            if warehouses:

                warehouses_serializer = WareHouseSerializer(warehouses,many=True)
                warehouse_data = warehouses_serializer.data

            else:

                warehouse_data = []



            try:

                warehouses = Shop.objects.filter(specification_id=specification_id)

            except:

                warehouses = None


            if warehouses:

                warehouses_serializer = ShopSerializer(warehouses,many=True)
                shop_data = warehouses_serializer.data

            else:

                shop_data = []


        else:
            warehouse_data = []
            shop_data = [] 


    else:
        warehouse_data = []
        shop_data = []



    return JsonResponse({'success':True,'message':'Data is shown below','warehouse_data':warehouse_data,'shop_data':shop_data})


@api_view(["POST",])
def subtract_quantity(request, order_details_id):


    warehouse_id = request.data.get("warehouse_id")
    shop_id = request.data.get("shop_id")
    quantity = request.data.get("quantity")
    quantity = int(quantity)


    if warehouse_id is None:

        inventory_id = shop_id


        try:

            product = OrderDetails.objects.get(id=order_details_id)

        except:

            product = None 


        if product:

            item_quantity = product.total_quantity
            item_remaining = product.remaining

            if item_remaining > 0:

                #make the subtraction

                check = item_remaining - int(quantity)

                if check >= 0:

                    print("quantity thik dise")

                    product.remaining -= quantity
                    product.save()
                    item_remaining = product.remaining
                    item_quantity = product.quantity

                    try:
                        shop = Shop.objects.get(id=shop_id)

                    except:

                        shop = None

                    if shop:

                        shop.product_quantity -= quantity
                        shop.save()
                        shop_serializer = ShopSerializer(shop,many=False)
                        shop_data = shop_serializer.data


                    else:

                        shop_data = {}

                        




                    return JsonResponse({'success':True,'message':'The amount has been subtracted','remaining':item_remaining,'quantity':item_quantity,'shop_data':shop_data})



                else:

                    print("quantity thik dey nai")

                    return JsonResponse({'success':False,'message':'Enter the correct quantity','remaining':item_remaining,'quantity':item_quantity})


            else:

                print("item nai ar")

                return JsonResponse({'success':False,'message':'The items quantity has already been subtracted'})



        else:
             print("product nai")

             return JsonResponse({'success':False,'message':'The item does not exist'})

        


    elif shop_id is None:

        print("warehouse ase")

        inventory_id = warehouse_id

        print(inventory_id)


        try:

            product = OrderDetails.objects.get(id=order_details_id)

        except:

            product = None 


        if product:


            item_quantity = product.total_quantity
            item_remaining = product.remaining

            if item_remaining > 0:

                #make the subtraction

                check = item_remaining - quantity

                if check >= 0:

                    print("quantity thik dise")

                    product.remaining -= quantity
                    product.save()
                    item_remaining = product.remaining
                    item_quantity = product.quantity

                    try:
                        warehouse = Warehouse.objects.get(id=warehouse_id)

                    except:

                        warehouse = None

                    if warehouse:

                        warehouse.product_quantity -= quantity
                        warehouse.save()
                        warehouse_serializer = WareHouseSerializer(warehouse,many=False)
                        warehouse_data = warehouse_serializer.data


                    else:

                        warehouse_data = {}




                    return JsonResponse({'success':True,'message':'The amount has been subtracted','remaining':item_remaining,'quantity':item_quantity,'warehouse_data':warehouse_data})



                else:
                    print("quantity thik dey nai")

                    return JsonResponse({'success':False,'message':'Enter the correct quantity','remaining':item_remaining,'quantity':item_quantity})


            else:

                print("product er item nai")

                return JsonResponse({'success':False,'message':'The items quantity has already been subtracted'})



        else:
            print("item tai nai")

            return JsonResponse({'success':False,'message':'The item does not exist'})



@api_view(["POST",])    
def subtract_items(request,order_details_id):

#     data= {"warehouse": [
#         {
#             "id": 6,
#             "name": "WarehouseA",
#             "location": "Dhanmondi",
#             "subtract": 5
#         },
#         {
#             "id": 7,
#             "name": "WarehouseB",
#             "location": "Gulshan",
#             "subtract": 6
#         }
#     ],
#     "shop": [
#         {
#             "id": 2,
#             "name": "ShopB",
#             "location": "gulshan",
#             "subtract": 4
#         },
#         {
#             "id": 4,
#             "name": "ShopA",
#             "location": "Banani",
#             "subtract": 5
#         }
#     ]
# }


    data = request.data

    
    # print(data["warehouse"])
    # print(len(data["warehouse"]))
    # print(data["shop"])
    # print(len(data["warehouse"]))
    # print(data["warehouse"][0]["warehouse_id"])

    warehouse_data = data["warehouse"]
    shop_data = data["shop"]
    # print(warehouse_data)
    # print(len(warehouse_data))
    # print(warehouse_data[1]["warehouse_id"])

    #This is for the warehouse data

    try:

        item = OrderDetails.objects.get(id = order_details_id)


    except:

        item = None 


    if item:

        #Checking if any item has been subtracted from the warehouse

        item_remaining = item.remaining
        item_product_id = item.product_id
        item_color = item.product_color
        item_size = item.product_size

        try:

            spec = ProductSpecification.objects.get(product_id=item_product_id,color=item_color,size=item_size)

        except:

            spec = None 

        if spec:

            specification_id = spec.id

        else:

            specification_id = 0 

        if int(len(warehouse_data)) > 0:

            #looping through the warehouse items

            for i in range(int(len(warehouse_data))):

                if item_remaining > 0:

                    #fetch the warehouseinfo 

                    warehouse_id = warehouse_data[i]["id"]

                    subtract = int(warehouse_data[i]["subtract"])

                    try:

                        warehouse_info = WarehouseInfo.objects.get(warehouse_id=warehouse_id,specification_id=specification_id)

                    except:

                        warehouse_info = None

                    if warehouse_info:

                        if warehouse_info.quantity >= subtract:

                            warehouse_info.quantity -= subtract
                            warehouse_info.save()
                            item.remaining -= subtract
                            item.save()
                            item_remaining = item.remaining
                            if item_remaining == 0:


                                return JsonResponse({"success":True,"message":"This product is approved"})




                        else:
                            return JsonResponse({"success":False,"message":"The warehouse does not have enough of this item"})

                    else:
                        return JsonResponse({"success":False,"message":"The warehouse does not have enough of this item"})


                # elif item_remaining==0:

                #     return JsonResponse({"success":True,"message":"This product is approved"})





                else:
                    return JsonResponse({"success":False,"message":"These many items dont exist in this order"})



        else:

            pass


        if int(len(shop_data)) > 0:

            #looping through the warehouse items

            for i in range(int(len(shop_data))):

                print("loop er moddhe dhuklam")

                if item_remaining > 0:

                    print("shop item_remaining ase")

                    #fetch the warehouseinfo 

                    shop_id = shop_data[i]["id"]

                    subtract = int(shop_data[i]["subtract"])

                    try:

                        shop_info = ShopInfo.objects.get(shop_id= shop_id,specification_id=specification_id)

                    except:

                        shop_info = None

                    if shop_info:

                        if shop_info.quantity >= subtract:

                            shop_info.quantity -= subtract
                            shop_info.save()

                            print("shoper aager")

                            print(item_remaining)

                            item.remaining -= subtract
                            item.save()
                            item_remaining = item.remaining

                            print("shop er porer")

                            print(item_remaining)

                            if item_remaining == 0:


                                return JsonResponse({"success":True,"message":"This product is approved"})

                            

                        else:
                            return JsonResponse({"success":False,"message":"The shop does not have enough of this item"})

                    else:
                        return JsonResponse({"success":False,"message":"The shop does not have enough of this item"})

                # elif item_remaining==0:

                #     return JsonResponse({"success":True,"message":"This product is approved"})



                else:
                    return JsonResponse({"success":False,"message":"These many items dont exist in this order"})



        else:

            pass







    else:

        JsonResponse({"success":False,"message":"The item is not in that order"})

        


@api_view(["POST",])
def admin_approval(request,order_id):

    flag = 0



    try:

        specific_order = Order.objects.get(id=order_id)

    except:

        specific_order = None

    if specific_order:

        orderid = specific_order.id

        order_details = OrderDetails.objects.filter(order_id=orderid)
        order_details_ids = list(order_details.values_list('id',flat=True).distinct())
        print(order_details_ids)

        for i in range(len(order_details_ids)):

            print("ashtese")

            try:
                specific_order_details = OrderDetails.objects.get(id=order_details_ids[i])
            except:
                specific_order_details = None

            if specific_order_details:

                remaining_items = specific_order_details.remaining

                if remaining_items != 0 :

                    flag = 1
                    break

                else:

                    flag = 0



        if flag == 0:

            specific_order.admin_status = "Confirmed"
            specific_order.save()

            return JsonResponse({'success':True,'message':'The order has been approved'})

        else:

            return JsonResponse({'success':False,'message':'Please ensure where to remove the items from'})


    else:

        return JsonResponse({'success':False,'message':'The order does not exist'})
































@api_view(["GET", "POST"])
def confirm_products(request):
    values = {
        "order_id" : 1,
        "quantity": 2000000,
        "store": "warehouse",
        "ware_name": "sheba.xyz",
        "ware_house_id": 1
    }

    if(request.method == "POST"):

        ware_house = []
        shops = []
        flag =0
        reminder = -1
        
        try:
            
            order_info = OrderDetails.objects.filter(order_id=values['order_id'])
            for orders in order_info:
                all_quantity_data = OrderDetails.objects.get(product_id=orders.product_id, product_size=orders.product_size, product_color=orders.product_color)
                specific_quantity = all_quantity_data.total_quantity
                if(values['quantity']>specific_quantity):
                    flag= flag+1
                else:
                    print("specific quantity", specific_quantity)
                    if (values['store']== "warehouse"):
                        ware_house_info = Warehouse.objects.get(id = values['ware_house_id'])
                        quantity = ware_house_info.product_quantity
                        if(values['quantity']>quantity):
                            flag= flag+1
                        else:
                            print("before add", ware_house_info.product_quantity)
                            ware_house_info.product_quantity = (quantity - values['quantity'])
                            ware_house_info.save()
                            print("after add", ware_house_info.product_quantity)
                            reminder = specific_quantity-values['quantity']
                    
                    elif (values['store']== "shop"):
                        shop_house_info = Shop.objects.get(id = values['ware_house_id'])
                        quantity = shop_house_info.product_quantity
                        if(values['quantity']>quantity):
                            flag= flag+1
                        else:
                            shop_house_info.product_quantity = (quantity - values['quantity'])
                            shop_house_info.save()
                            reminder = specific_quantity-values['quantity']

            if(reminder<0):
                reminder = 0
        
        except:
            return Response({'Message': 'Check whether requested data exists or not'})

        
        if (flag>0):
            return Response({
                "success": False,
                "Message": "You set wrong values !!"
            })
        else:
            return Response({
                "success": True,
                "Message": "Information has been updated",
                "reminder": reminder
            })






@api_view(["POST",])
def create_warehouse(request):


    serializer = WarehouseSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({"success":True,"message":"Warehouse has been created","data":serializer.data})


    else:

        return Response({"success":True,"message":"Warehouse could not be created"})





@api_view(["POST",])
def create_shop(request):


    serializer = ShopSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({"success":True,"message":"Shop has been created","data":serializer.data})


    else:

        return Response({"success":True,"message":"Shop could not be created"})



@api_view(["POST",])
def update_shop(request,shop_id):


    try:

        shop = Shop.objects.get(id = shop_id)


    except:

        shop = None

    if shop:

        serializer = ShopSerializer(shop,data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"success":True,"message":"Shop data has been updated","data":serializer.data})


        else:

            return Response({"success":True,"message":"Shop data could not be updated"})


    else:

        return Response({"success":True,"message":"Shop does not exist"})





@api_view(["POST",])
def update_warehouse(request,warehouse_id):


    try:

        warehouse = Warehouse.objects.get(id = warehouse_id)


    except:

        warehouse = None

    if warehouse:

        serializer = WarehouseSerializer(warehouse,data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"success":True,"message":"Warehouse data has been updated","data":serializer.data})


        else:

            return Response({"success":True,"message":"Warehouse data could not be updated"})


    else:

        return Response({"success":True,"message":"Warehouse does not exist"})



@api_view(["GET",])
def show_all_warehouses(request):


    try:

        warehouse = Warehouse.objects.all()

    except:

        warehouse = None 

    if warehouse:

        serializer = WarehouseSerializer(warehouse,many=True)
        return Response({"success":True,"message":"Data is shown","data":serializer.data})

    else:

        return Response({"success":False,"message":"No data could be retrieved","data": []})



@api_view(["GET",])
def show_all_shops(request):


    try:

        warehouse = Shop.objects.all()

    except:

        warehouse = None 

    if warehouse:

        serializer = ShopSerializer(warehouse,many=True)
        return Response({"success":True,"message":"Data is shown","data":serializer.data})

    else:

        return Response({"success":False,"message":"No data could be retrieved","data": []})



def delete_warehouse(request,warehouse_id):


    try:

        warehouse = Warehouse.objects.get(id = warehouse_id)

    except:

        warehouse = None 



    if warehouse:

        warehouse.delete()
        return JsonResponse({"success":True,"message":"Warehouse has been deleted"})

    else:
        return JsonResponse({"success":False,"message":"Warehouse does not exist"})





def delete_shop(request,shop_id):


    try:

        warehouse = Shop.objects.get(id = shop_id)

    except:

        warehouse = None 



    if warehouse:

        warehouse.delete()
        return JsonResponse({"success":True,"message":"Shop has been deleted"})

    else:
        return JsonResponse({"success":False,"message":"Shop does not exist"})









@api_view(["GET",])
def inventory_lists(request, order_details_id):


    try:

        product = OrderDetails.objects.get(id=order_details_id)

    except:

        product = None 


   


    if product:


        product_id = product.product_id
        product_size = product.product_size
        product_color = product.product_color



        try:

            spec = ProductSpecification.objects.get(
                    product_id=product_id, size=product_size, color=product_color) 


        except:

            spec = None 




        if spec:

            specification_id = spec.id
            print(specification_id) 


            try:

                warehouses = WarehouseInfo.objects.filter(specification_id=specification_id)

            except:

                warehouses = None


            print(warehouses)


            warehouse_infos = []





            if warehouses:

                warehouse_ids = list(warehouses.values_list('warehouse_id',flat=True))
                warehouse_quantities = list(warehouses.values_list('quantity',flat=True))

                for i in range(len(warehouse_ids)):

                    try:
                        warehouse = Warehouse.objects.get(id = warehouse_ids[i])
                    except:
                        warehouse = None

                    if warehouse:



                        name = warehouse.warehouse_name
                        location = warehouse.warehouse_location
                        quantity = warehouse_quantities[i]

                        warehouse_data = {"id":warehouse_ids[i],"name":name,"location":location,"quantity":quantity}

                    else:

                        warehouse_data = {}



                    warehouse_infos.append(warehouse_data)


            else:

                warehouse_infos = []




            try:

                shops = ShopInfo.objects.filter(specification_id=specification_id)

            except:

                shops = None


            


            shop_infos = []





            if shops:

                shop_ids = list(shops.values_list('shop_id',flat=True))
                shop_quantities = list(shops.values_list('quantity',flat=True))

                for i in range(len(shop_ids)):

                    try:
                        shop = Shop.objects.get(id = shop_ids[i])
                    except:
                        shop = None

                    if warehouse:

                        name = shop.shop_name
                        location = shop.shop_location
                        quantity = shop_quantities[i]

                        shop_data = {"id":shop_ids[i],"name":name,"location":location,"quantity":quantity}

                    else:

                        shop_data = {}



                    shop_infos.append(shop_data)


            else:

                shop_infos = []


        else:
            warehouse_infos = []
            shop_infos = []



    return JsonResponse({'success':True,'message':'Data is shown below','warehouse':warehouse_infos,'shop':shop_infos})



@api_view(["GET",])
def warehouse_products(request,warehouse_id):

    try:

        products =  Warehouse.objects.get(id=warehouse_id)

    except:

        products = None 


    if products: 

        warehouse_serializer = WarehouseSerializer(products,many=False)
        warehouse_data = warehouse_serializer.data
        return JsonResponse({'success':True,'message':'Here is the data','data':warehouse_data})

    else:

        warehouse_data = {}
        return JsonResponse({'success':False,'message':'Here is the data','data':warehouse_data})

@api_view(["GET",])
def shop_products(request,shop_id):

    try:

        products =  Shop.objects.get(id=shop_id)

    except:

        products = None 


    if products: 

        warehouse_serializer = ShopSerializer(products,many=False)
        warehouse_data = warehouse_serializer.data
        return JsonResponse({'success':True,'message':'Here is the data','data':warehouse_data})

    else:

        warehouse_data = {}
        return JsonResponse({'success':False,'message':'Here is the data','data':warehouse_data})

# ----------------------------------- quantity store in different shop/inventory ------------------------

@api_view (["GET","POST"])
def insert_product_quantity(request):

    # demo values
    api_values = {
        'product_id': 2,
        'specification_id':8,
        'warehouse': [
            {
                'warehouse_id': 2,
                'quantity': 200

            },
            {
                'warehouse_id': 3,
                'quantity': 400

            }
            
        ],

         'shop': [
            {
                'shop_id': 2,
                'quantity': 200

            },
            {
                'shop_id': 3,
                'quantity': 300

            }
            
        ]
        
        }

  

    if request.method == 'POST':
      
        try:
            
            # checking is there any warehouse data exists or not
            if len(api_values['warehouse'])>0 :
                for wareh in api_values['warehouse']:
                    try:
                        # getting the previous data if there is any in the similar name. If exists update the new value. if does not create new records.
                        wareh_query = WarehouseInfo.objects.filter(warehouse_id = wareh['warehouse_id'], specification_id = api_values['specification_id'])
                        if wareh_query.exists():
                            quantity_val = wareh_query[0].quantity
                            new_quantity = quantity_val+ wareh['quantity']
                            wareh_query.update(quantity=new_quantity)
                            
                        else:
                            wareh_data = WarehouseInfo(specification_id= api_values['specification_id'], product_id=  api_values['product_id'], warehouse_id = wareh['warehouse_id'],
                                                        quantity = wareh['quantity'] )
                            wareh_data.save()

                        # updating the inventory report credit records for each ware house quantity. It will help to keep the records in future.
                        report_data = inventory_report(product_id=api_values['product_id'],credit= wareh['quantity'],warehouse_id = wareh['warehouse_id'])
                        report_data.save()
                    except:
                        pass

            if len(api_values['shop'])>0 :
                for shops in api_values['shop']:
                    try:
                        # getting the existing shop values if is there any.
                        shop_query = ShopInfo.objects.filter(shop_id = shops['shop_id'], specification_id = api_values['specification_id'])
                        if shop_query.exists():
                            quantity_val = shop_query[0].quantity
                            new_quantity = quantity_val+ shops['quantity']
                            shop_query.update(quantity=new_quantity)
                        else:
                            shop_data = ShopInfo(specification_id= api_values['specification_id'], product_id=  api_values['product_id'], shop_id = shops['shop_id'],
                                                        quantity = shops['quantity'] )
                            shop_data.save()
                        # Updating the report table after being inserted the quantity corresponding to credit coloumn for each shop.
                        report_data = inventory_report(product_id=api_values['product_id'],credit= shops['quantity'],shop_id = shops['shop_id'])
                        report_data.save()
                    except:
                        pass
            
            return Response ({
                "success": True,
                "message": "Data has been added successfully"
            })
        except:
              return Response ({
                "success": False,
                "message": "Something went wrong !!"
            })
    
           
           
