from django.shortcuts import render
import json
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
# from api.models import Contact, ContactSerializer
from api.models import Books, Profile, Inventory, Trades
from api.models import BooksSerializer, ProfileSerializer, InventorySerializer, TradesSerializer
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.permissions import AllowAny, IsAuthenticated

# class ContactsView(APIView):
#     def get(self, request, contact_id=None):

#         if contact_id is not None:
#             contact = Contact.objects.get(id=contact_id)
#             serializer = ContactSerializer(contact, many=False)
#             return Response(serializer.data)
#         else:
#             contacts = Contact.objects.all()
#             serializer = ContactSerializer(contacts, many=True)
#             return Response(serializer.data)
        
#     def post(self, request):
            
#         serializer = ContactSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_200_OK)
#         else:
#             return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            
        
#     def delete(self, request, contact_id):
        
#         contact = Contact.objects.get(id=contact_id)
#         contact.delete()
        
#         return Response(status=status.HTTP_204_NO_CONTENT)
class BooksView(APIView):
    def get(self, request, book_id=None):
        if book_id is not None:
            book = Books.objects.get(id=book_id)
            serializer = BooksSerializer(book, many=False)
            return Response(serializer.data)
        else:
            book = Books.objects.all()
            serializer = BooksSerializer(book, many=True)
            return Response(serializer.data)
        
class RequestsView(APIView):
    def get(self, request, profile_id):
        user_books = Inventory.objects.get(id=profile_id)
        requests = [user_books.id for user_books in Trades.objects.all()]
        
        return Response(requests)
        
    
    def post(self, request):
        serializer = TradesSerializer(data=request.data)
        if serializer.is_valid():
          serializer.save()
          return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            

        
# class TradesView(APIView):
#     def get(self, request, profile_id):
#         trader = Trades.objects.get(profile=profile_id)
#         trades = [ in Trades.objects.all()]
        
        
#     def put(self, request, profile_id):
#         trade = Trades.objects.get(id=profile_id)
#          trade.is_accepted = request.data.get("is_accepted")
#          trade.save()
        
#          serializer = TradesSerializer(data=request.data)
#          if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_200_OK)
#          else:
#             return Response(serializer.data, status=status.HTTP_400_BAD_REQUEST)
            
    
#     def delete(self, request, profile_id):
#         trade = Trades.objects.get(id=profile_id)
#         trade.delete()
        
#         return Response(status=status.HTTP_204_NO_CONTENT)
        