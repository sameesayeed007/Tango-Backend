from rest_framework import serializers

from django.contrib.auth.models import User
from Intense.models import Advertisement
from django.conf import settings




# Serializers define the API representation.
# host_prefix = "http://"
# host_name = host_prefix+settings.ALLOWED_HOSTS[0]+":8080"

host_prefix = "https://"
host_name = host_prefix+settings.ALLOWED_HOSTS[0]

class AdvertisementSerializer(serializers.ModelSerializer):
	image_url = serializers.SerializerMethodField(method_name='get_image')
	class Meta: 
		model = Advertisement
		fields =('id','ad_link','priority','image','image_url','content','click_count','view_count','total_click_count','total_view_count','is_active')
    

	def get_image(self,instance):



		try:

			logo_image = Advertisement.objects.get(id = instance.id)

		except:
			logo_image = None

		if logo_image is not None:
			if logo_image.image:

				logo = logo_image.image
				return "{0}{1}".format(host_name,logo.url)

		else:
			return " "





