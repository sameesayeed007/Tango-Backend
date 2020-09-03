from rest_framework import serializers
from Intense.models import Ticket,TicketReplies,User


# Serializers define the API representation.
class TicketSerializer(serializers.ModelSerializer):
    replies = serializers.SerializerMethodField(method_name='all_replies')
    sender_name = serializers.SerializerMethodField(method_name='ticket_sender')
    attender_name= serializers.SerializerMethodField(method_name='ticket_attender')
    class Meta:
        model = Ticket
        fields = ('id','title','sender_id','sender_name','receiver_id','attender_name','department', 'status','complain','created', 'modified','is_active','replies')

    def all_replies(self, obj):
        all_replies=[]
        replies = TicketReplies.objects.filter(ticket_id=obj.id).values()
        for rep in replies:
            try:
                senders = User.objects.filter(id= rep['user_id']).values('email')
                rep.update({'sender':senders[0]['email']})
            except:
                pass
            all_replies.append(rep)
        return all_replies

    def ticket_sender (self,obj):
        try:
            sender = User.objects.get(id= obj.sender_id)
            return sender.email
        except:
            return {"message": "User could not find"}

    def ticket_attender (self, obj):
        try:
            receiver = User.objects.get(id= obj.receiver_id)
            return receiver.email
        except:
            return {"message": "Attender is not decided yet"}


class TicketRepliesSerializer(serializers.ModelSerializer):
    attender_name = serializers.SerializerMethodField(method_name='attender_reply')
    class Meta:
        model = TicketReplies
        fields = ('id','ticket_id','reply','created','user_id','attender_name')

    def attender_reply (self, obj):
        try:
            receiver = User.objects.get(id= obj.user_id)
            return receiver.email
        except:
            return {"message": "Problem while retrieving attender name"}

