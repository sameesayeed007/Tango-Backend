from django.shortcuts import render

from django.http.response import JsonResponse
from rest_framework.parsers import JSONParser 
from rest_framework import status
 
from Intense.models import Ticket, TicketReplies,User
from .serializers import TicketSerializer ,TicketRepliesSerializer
from rest_framework.decorators import api_view 
from django.views.decorators.csrf import csrf_exempt

#shows all the tickets and the replies of that specific ticket
#This is for the admin
@api_view(['GET',])
def ticket_list(request):

	try:
		tickets = Ticket.objects.all()
		ticketserializer = TicketSerializer(tickets,many=True)
		return JsonResponse(
			{
				'success': True,
				'message': 'Data has been retrieved successfully',
				'data':ticketserializer.data
			}, safe=False)

	except Ticket.DoesNotExist:
		return JsonResponse({
			'success': False,
			'message': 'The ticket does not exist'}, status=status.HTTP_404_NOT_FOUND)


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
		return JsonResponse({
			'success':True,
			'message': 'data has been retrived successfully',
			'data': ticketserializer.data
		}, safe=False)

	except Ticket.DoesNotExist:
		return JsonResponse({
			'success': False,
			'message': 'The ticket does not exist'
			}, status=status.HTTP_404_NOT_FOUND)
    

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
		ticket_data = ticketserializer.data
		return JsonResponse({
			'success': True,
			'message': "Data has been retrived successfully",
			'data':ticket_data
		}, safe=False)

	except Ticket.DoesNotExist:
		return JsonResponse({
			'success': False,
			'message': 'The ticket does not exist'
			}, status=status.HTTP_404_NOT_FOUND)


#Shows all the tickets of a specific user
@api_view(['GET',])
def sender_ticket(request,sender_id):
	user = User.objects.filter(id=sender_id)
	if user.exists():
		try:
			tickets = Ticket.objects.filter(sender_id=sender_id)
			ticketid = tickets.values_list('id' , flat = True)
			replies = []
			for i in range(len(ticketid)):
				ticketreplies = TicketReplies.objects.filter(ticket_id=ticketid[i])
				replies += ticketreplies

			
			ticketserializer = TicketSerializer(tickets,many=True)
			ticketrepliesserializer = TicketRepliesSerializer(replies,many=True)
			return JsonResponse({
				'success': True,
				'message': "data has been retrived successfully",
				'data':ticketrepliesserializer.data
			}, safe=False)

		except Ticket.DoesNotExist:
			return JsonResponse({
				'success': False,
				'message': 'The ticket does not exist'
				}, status=status.HTTP_404_NOT_FOUND)

	else:
		return JsonResponse({
				'success': False,
				'message': 'This user does not have any ticket'
				}, status=status.HTTP_404_NOT_FOUND)

#Shows all the tickets handled by a specific receiver
@api_view(['GET',])
def receiver_ticket(request,receiver_id):

	user = User.objects.filter(id=receiver_id)
	if user.exists():
		try:
			tickets = Ticket.objects.filter(receiver_id=receiver_id)
			ticketid = tickets.values_list('id' , flat = True)
			replies = []
			for i in range(len(ticketid)):
				ticketreplies = TicketReplies.objects.filter(ticket_id=ticketid[i])
				replies += ticketreplies

			ticketserializer = TicketSerializer(tickets,many=True)
			ticketrepliesserializer = TicketRepliesSerializer(replies,many=True)
			return JsonResponse({
				'success': True,
				'message': 'data has been retrived successfully',
				'data': ticketrepliesserializer.data
			}, safe=False)

		except Ticket.DoesNotExist:
			return JsonResponse({
				'success': False,
				'message': 'The ticket does not exist'}, status=status.HTTP_404_NOT_FOUND)
	else:
		return JsonResponse({
				'success': False,
				'message': 'There is no ticket for this receiver'}, status=status.HTTP_404_NOT_FOUND)

#This creates a ticket 
@api_view(['POST',])
def create_ticket(request):
	ticket_serializer = TicketSerializer(data=request.data)
	if ticket_serializer.is_valid():
		ticket_serializer.save()
		return JsonResponse({
			'success': True,
			'message': 'Data has been retrieved successfully',
			'data': ticket_serializer.data
		}, status=status.HTTP_201_CREATED)
	return JsonResponse ({
		'success': False,
		'message': 'Ticket could not be created',
		'error': ticket_serializer.errors
	})

#This updates a ticket info. The admin or support can add the receiver info and the department
@api_view(['POST',])
def edit_ticketinfo(request,ticket_id):

	try:
		comment = Ticket.objects.get(id = ticket_id)
		if request.method == 'POST':
			commentserializer = TicketSerializer(comment , data=request.data )
			if commentserializer.is_valid():
				commentserializer.save()
				return JsonResponse({
					'success': True,
					'message': 'Information has been updated successfully',
					'data': commentserializer.data
				})
			return JsonResponse ({
				'success': False,
				'message': 'Information could not be updated',
				'error': commentserializer.errors
			})
	except Ticket.DoesNotExist:
		return JsonResponse({
			'success': False,
			'message': 'This ticket does not exist'}, status=status.HTTP_404_NOT_FOUND)


@api_view(['POST',])
#Creates a reply for a specific ticket reply
def create_reply(request):

	ticketreplies_serializer = TicketRepliesSerializer(data=request.data)
	if ticketreplies_serializer.is_valid():

		ticketreplies_serializer.save()
		return JsonResponse({
			'success': True,
			'message': 'Reply has been created successfully',
			'data': ticketreplies_serializer.data
		}, status=status.HTTP_201_CREATED)	
	return JsonResponse({
		'success': False,
		'message': 'Reply could not be created',
		'error': ticketreplies_serializer.errors
	}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST',])
def edit_ticketreply(request,reply_id):
	
	comm = TicketReplies.objects.filter(pk = reply_id)
	if comm.exists():
		try:
			comment = TicketReplies.objects.get(pk = reply_id)
			if request.method == 'POST':
				commentserializer = TicketRepliesSerializer(comment , data=request.data )
				if commentserializer.is_valid():
					commentserializer.save()
					return JsonResponse({
						'success': True,
						'message': 'Reply has been updated successfully',
						'data': commentserializer.data
					})
				return JsonResponse({
					'success': False,
					'message': 'Problem while updating reply',
					'error': commentserializer.errors
				}, status=status.HTTP_400_BAD_REQUEST)

		except Ticket.DoesNotExist:
			return JsonResponse({
				'success': False,
				'message': 'This ticket reply does not exist'}, status=status.HTTP_404_NOT_FOUND)
	else:
		return JsonResponse({
				'success': False,
				'message': 'Invalid reply id'}, status=status.HTTP_404_NOT_FOUND)


#Delete a certain ticket
@api_view(['POST',])
def delete_ticket(request,ticket_id):

	tickets = Ticket.objects.filter(pk = ticket_id)
	ticketreplies = TicketReplies.objects.filter(ticket_id = ticket_id)
	if request.method == 'POST':
		if tickets.exists():
			tickets.delete()
			ticketreplies.delete()
			return JsonResponse({
				'success': True,
				'message': 'Ticket was deleted successfully!'}, status=status.HTTP_204_NO_CONTENT)
		else:

			return JsonResponse({
				'success': False,
				'message': 'Could not be deleted'
				})

