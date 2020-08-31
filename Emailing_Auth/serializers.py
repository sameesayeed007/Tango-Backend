from rest_framework import serializers

from django.contrib.auth.models import User
from Intense.models import EmailConfig

class EmailConfigSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmailConfig
        fields = "__all__"