from rest_framework import serializers

from django.contrib.auth.models import User
from Intense.models import Ticket,TicketReplies


# Serializers define the API representation.
class TicketSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ticket
        fields = ('id','title','sender_id','receiver_id','department', 'status','complain','created', 'modified','is_active')



class TicketRepliesSerializer(serializers.ModelSerializer):
    class Meta:
        model = TicketReplies
        fields = ('id','ticket_id','reply','created','user_id')


