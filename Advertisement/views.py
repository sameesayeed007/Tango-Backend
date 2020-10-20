from django.shortcuts import render
from django.http import HttpResponse
from django.http.response import JsonResponse
from rest_framework.parsers import JSONParser 
from rest_framework import status
import datetime
 
from Intense.models import Advertisement
from .serializers import AdvertisementSerializer
from rest_framework.decorators import api_view 
from django.views.decorators.csrf import csrf_exempt


#This creates an ad
@api_view(['POST',])
def add_ad(request):
		
	adsserializer = AdvertisementSerializer(data=request.data)
	if adsserializer.is_valid():
		adsserializer.save()
		return JsonResponse({
			'success': True,
			'message': 'Successfully added the advertisement',
			'data':adsserializer.data
		}, status=status.HTTP_201_CREATED)

	return JsonResponse({
		'success': False,
		'message': 'Advertisment value could not be inserted.',
		'data':adsserializer.errors
	})

#Shows information about a specific ad
@api_view(['GET',])
def show_ad(request,ad_id):

	try:
		ad = Advertisement.objects.get(id = ad_id)
		adserializer = AdvertisementSerializer(ad,many=False)
		return JsonResponse({
			'success': True,
			'message': 'Advertisement data has been retrieved successfully',
			'data': adserializer.data
		},safe=False)

	except Advertisement.DoesNotExist:
		return JsonResponse({
			'success': False,
			'message': 'This Advertisement does not exist'
			}, status=status.HTTP_404_NOT_FOUND)




#This shows all the ad
@api_view(['GET',])
def show_all_ads(request):

	try:
		ad1 = Advertisement.objects.filter(priority=2,is_active=True)

	except:

		ad1 = None

	if ad1:
		
		adserializer = AdvertisementSerializer(ad1,many=True)
		data = adserializer.data 

	else:

		data = [] 

	try:
		ad2 = Advertisement.objects.filter(priority=1,is_active=True)

	except:

		ad2 = None

	if ad2:

		adserializer1 = AdvertisementSerializer(ad2,many=True)
		data1 = adserializer1.data


	else:

		data1 = []



	return JsonResponse({
		'success': True,
		'message': 'Data has been retrived successfully',
		'data': data,
		'data1' : data1
	},safe=False)

@api_view(['GET',])
def admin_ads(request):

	try:

		ad = Advertisement.objects.all()

	except:

		ad = None

	if ad:

		adserializer = AdvertisementSerializer(ad,many=True)
		data = adserializer.data
		return JsonResponse({"success":True,"message":"Data is shown","data": data})

	else:

		data = []

		return JsonResponse({"success":False,"message":"Data could not be retrived","data": data})


@api_view (["POST",])
def change_status(request,ad_id):

    try:
        ad = Advertisement.objects.get(pk=ad_id)


    # print(ad)

    except:

        ad = None 


    print(ad)





  

    if ad:

        ad_status = ad.is_active
        
        if ad_status == True:
            ad.is_active = False
            ad.save()

        elif ad_status == False:

            ad.is_active = True
            ad.save()

        


        serializers = AdvertisementSerializer(ad,many = False)
        # banner_ids = banner.values_list('id' , flat = True)
        # image_serializers = []
        # for i in range(len(banner_ids)):

        #     try:
        #         banner_image = Banner_Image.objects.filter(Banner_id = banner_ids[i])
        #     except:
        #         banner_image = None
        #     if banner_image is not None:
        #         image_serializer = BannerImageSerializer (banner_image,many = True)
        #         image_serializers += image_serializer.data



        return JsonResponse({'success': True,
                'message': 'The values are inserted below',
                'ad_data': serializers.data})
                # 'images' : image_serializers})


    else:

        return JsonResponse({'success':False,'message':'the ad does not exist'})




#This updates the latest product specification
@api_view(['POST',])
def update_ad(request,ad_id):

	try:
		ad = Advertisement.objects.get(id=ad_id)
		try:
			
			click_count = int(request.data.get('click_count'))
			view_count = int(request.data.get('view_count'))

			ad.total_view_count += view_count
			ad.total_click_count += click_count
			ad.save()
		except:
			pass


		if request.method == 'POST':
			adserializer = AdvertisementSerializer(ad,data=request.data)
			if adserializer.is_valid():
				adserializer.save()

			return JsonResponse({
				'success': True,
				'message': 'Data has been retrived successfully',
				'data': adserializer.data
			}, status=status.HTTP_201_CREATED)

	except Advertisement.DoesNotExist:
		return JsonResponse({
			'success': False,
			'message': 'This advertisement does not exist'
			}, status=status.HTTP_404_NOT_FOUND)


#This deletes an ad 
@api_view(['POST',])
def delete_ad(request,ad_id):

	try:
		ad = Advertisement.objects.get(id = ad_id)
		ad.delete()
		return JsonResponse({
			'success': True,
			'message': 'This Advertisement has been deleted successfully'})


	except Advertisement.DoesNotExist:
		return JsonResponse({
			'success': False,
			'message': 'This Advertisement does not exist'}, status=status.HTTP_404_NOT_FOUND)
