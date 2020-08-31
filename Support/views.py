from django.shortcuts import render

from django.http.response import JsonResponse
from rest_framework.parsers import JSONParser 
from rest_framework import status
 
from Intense.models import Ticket, TicketReplies
from .serializers import TicketSerializer ,TicketRepliesSerializer
from rest_framework.decorators import api_view 
from django.views.decorators.csrf import csrf_exempt

#shows all the tickets and the replies of that specific ticket
#This is for the admin
@api_view(['GET',])
def ticket_list(request):

	try:
		tickets = Ticket.objects.all()
		ticketreplies = TicketReplies.objects.all()
		ticketserializer = TicketSerializer(tickets,many=True)
		ticketrepliesserializer = TicketRepliesSerializer(ticketreplies,many=True)
		ticket_data = [ticketserializer.data,ticketrepliesserializer.data]
		return JsonResponse(ticket_data, safe=False)

	except Ticket.DoesNotExist:
		return JsonResponse({'message': 'The ticket does not exist'}, status=status.HTTP_404_NOT_FOUND)


#Shows the ticket by a specific id and its replies
@api_view(['GET',])
def specific_ticket(request,ticket_id):

	try:
		tickets = Ticket.objects.filter(id = ticket_id)
		ticketid = tickets.values_list('id' , flat = True)
		replies = []
		for i in range(len(ticketid)):
			ticketreplies = TicketReplies.objects.filter(ticket_id=ticketid[i])
			replies += ticketreplies

		
		ticketserializer = TicketSerializer(tickets,many=True)
		ticketrepliesserializer = TicketRepliesSerializer(replies,many=True)
		ticket_data = [ticketserializer.data,ticketrepliesserializer.data]
		return JsonResponse(ticket_data, safe=False)

	except Ticket.DoesNotExist:
		return JsonResponse({'message': 'The ticket does not exist'}, status=status.HTTP_404_NOT_FOUND)
    

#Shows all the active tickets
@api_view(['GET',])
def active_ticket(request):

	try:
		tickets = Ticket.objects.filter(is_active=True)
		ticketid = tickets.values_list('id' , flat = True)
		replies = []
		for i in range(len(ticketid)):
			ticketreplies = TicketReplies.objects.filter(ticket_id=ticketid[i])
			replies += ticketreplies

		
		ticketserializer = TicketSerializer(tickets,many=True)
		ticketrepliesserializer = TicketRepliesSerializer(replies,many=True)
		ticket_data = [ticketserializer.data,ticketrepliesserializer.data]
		return JsonResponse(ticket_data, safe=False)

	except Ticket.DoesNotExist:
		return JsonResponse({'message': 'The ticket does not exist'}, status=status.HTTP_404_NOT_FOUND)


#Shows all the tickets of a specific user
@api_view(['GET',])
def sender_ticket(request,sender_id):

	try:
		tickets = Ticket.objects.filter(sender_id=sender_id)
		ticketid = tickets.values_list('id' , flat = True)
		replies = []
		for i in range(len(ticketid)):
			ticketreplies = TicketReplies.objects.filter(ticket_id=ticketid[i])
			replies += ticketreplies

		
		ticketserializer = TicketSerializer(tickets,many=True)
		ticketrepliesserializer = TicketRepliesSerializer(replies,many=True)
		ticket_data = [ticketserializer.data,ticketrepliesserializer.data]
		return JsonResponse(ticket_data, safe=False)

	except Ticket.DoesNotExist:
		return JsonResponse({'message': 'The ticket does not exist'}, status=status.HTTP_404_NOT_FOUND)


#Shows all the tickets handled by a specific receiver
@api_view(['GET',])
def receiver_ticket(request,receiver_id):

	try:
		tickets = Ticket.objects.filter(receiver_id=receiver_id)
		ticketid = tickets.values_list('id' , flat = True)
		replies = []
		for i in range(len(ticketid)):
			ticketreplies = TicketReplies.objects.filter(ticket_id=ticketid[i])
			replies += ticketreplies

		
		ticketserializer = TicketSerializer(tickets,many=True)
		ticketrepliesserializer = TicketRepliesSerializer(replies,many=True)
		ticket_data = [ticketserializer.data,ticketrepliesserializer.data]
		return JsonResponse(ticket_data, safe=False)

	except Ticket.DoesNotExist:
		return JsonResponse({'message': 'The ticket does not exist'}, status=status.HTTP_404_NOT_FOUND)

#This creates a ticket 
@api_view(['POST',])
def create_ticket(request):
	ticket_serializer = TicketSerializer(data=request.data)
	if ticket_serializer.is_valid():
		ticket_serializer.save()
		return JsonResponse(ticket_serializer.data, status=status.HTTP_201_CREATED)
	return JsonResponse (ticket_serializer.errors)

#This updates a ticket info. The admin or support can add the receiver info and the department
@api_view(['POST',])
def edit_ticketinfo(request,ticket_id):

	try:
		comment = Ticket.objects.get(id = ticket_id)
		if request.method == 'POST':
			commentserializer = TicketSerializer(comment , data=request.data )
			if commentserializer.is_valid():
				commentserializer.save()
				return JsonResponse(commentserializer.data)
			return JsonResponse (commentserializer.errors)
	except Ticket.DoesNotExist:
		return JsonResponse({'message': 'This ticket does not exist'}, status=status.HTTP_404_NOT_FOUND)


@api_view(['POST',])
#Creates a reply for a specific ticket reply
def create_reply(request):

	ticketreplies_serializer = TicketRepliesSerializer(data=request.data)
	if ticketreplies_serializer.is_valid():

		ticketreplies_serializer.save()
		return JsonResponse(ticketreplies_serializer.data, status=status.HTTP_201_CREATED)	
	return JsonResponse(ticketreplies_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST',])
def edit_ticketreply(request,reply_id):

	try:
		comment = TicketReplies.objects.get(pk = reply_id)
		if request.method == 'POST':
			commentserializer = TicketRepliesSerializer(comment , data=request.data )
			if commentserializer.is_valid():
				commentserializer.save()
				return JsonResponse(commentserializer.data)
			return JsonResponse(commentserializer.errors, status=status.HTTP_400_BAD_REQUEST)

	except Ticket.DoesNotExist:
		return JsonResponse({'message': 'This ticket reply does not exist'}, status=status.HTTP_404_NOT_FOUND)


#Delete a certain ticket
@api_view(['POST',])
def delete_ticket(request,ticket_id):

	tickets = Ticket.objects.filter(pk = ticket_id)
	ticketreplies = TicketReplies.objects.filter(ticket_id = ticket_id)
	if request.method == 'POST':
		if tickets.exists():
			tickets.delete()
			ticketreplies.delete()
			return JsonResponse({'message': 'Ticket was deleted successfully!'}, status=status.HTTP_204_NO_CONTENT)
		else:

			return JsonResponse({'message': 'The ticket does not exist'})

