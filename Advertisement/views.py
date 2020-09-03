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
		ad = Advertisement.objects.all()
		adserializer = AdvertisementSerializer(ad,many=True)
		return JsonResponse({
			'success': True,
			'message': 'Data has been retrived successfully',
			'data': adserializer.data
		},safe=False)

	except Advertisement.DoesNotExist:
		return JsonResponse({
			'success': False,
			'message': 'This Advertisement does not exist'}, status=status.HTTP_404_NOT_FOUND)



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
