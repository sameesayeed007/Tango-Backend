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

		values = {'view_count': '5'}
		adsserializer = AdvertisementSerializer(data=values)
		if adsserializer.is_valid():
			
			adsserializer.save()

		return JsonResponse(adsserializer.data, status=status.HTTP_201_CREATED)

#Shows information about a specific ad
@api_view(['GET',])
def show_ad(request,ad_id):

	try:
		ad = Advertisement.objects.filter(id = ad_id)
		adserializer = AdvertisementSerializer(ad,many=True)
		return JsonResponse(adserializer.data,safe=False)

	except Advertisement.DoesNotExist:
		return JsonResponse({'message': 'This Advertisement does not exist'}, status=status.HTTP_404_NOT_FOUND)


#This shows all the ad
@api_view(['GET',])
def show_all_ads(request):

	try:
		ad = Advertisement.objects.all()
		adserializer = AdvertisementSerializer(ad,many=True)
		return JsonResponse(adserializer.data,safe=False)

	except Advertisement.DoesNotExist:
		return JsonResponse({'message': 'This Advertisement does not exist'}, status=status.HTTP_404_NOT_FOUND)



#This updates the latest product specification
@api_view(['POST',])
def update_ad(request,ad_id):

	try:
		ad = Advertisement.objects.filter(id=ad_id).last()
		click_count = int(request.data.get('click_count'))
		view_count = int(request.data.get('view_count'))

		ad.total_view_count += view_count
		ad.total_click_count += click_count
		ad.save()


		if request.method == 'POST':
			adserializer = AdvertisementSerializer(ad,data=request.data)
			if adserializer.is_valid():
				adserializer.save()

			return JsonResponse(adserializer.data, status=status.HTTP_201_CREATED)

	except Advertisement.DoesNotExist:
		return JsonResponse({'message': 'This advertisement does not exist'}, status=status.HTTP_404_NOT_FOUND)


#This deletes an ad 
@api_view(['POST',])
def delete_ad(request,ad_id):

	try:
		ad = Advertisement.objects.filter(id = ad_id)
		ad.delete()
		return JsonResponse({'message': 'This Advertisement has been deleted'})


	except Advertisement.DoesNotExist:
		return JsonResponse({'message': 'This Advertisement does not exist'}, status=status.HTTP_404_NOT_FOUND)
