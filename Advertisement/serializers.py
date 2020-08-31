from rest_framework import serializers

from django.contrib.auth.models import User
from Intense.models import Advertisement




# Serializers define the API representation.

class AdvertisementSerializer(serializers.ModelSerializer):
	class Meta: 
		model = Advertisement
		fields =('id','ad_link','image','content','click_count','view_count','total_click_count','total_view_count','user_id','non_verfied_user_id','ip_address')
    





