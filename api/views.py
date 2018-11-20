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
    serializer_class = TradesSerializer
    
    def get(self, request, given_id):
        user_books = Trades.objects.filter(trader__profile=given_id)
        trades = TradesSerializer(user_books, many=True)
        return Response(trades.data)
        

class ProfileView(APIView):
    def get(self, request, profile_id, book_id):
        profile = Profile.objects.get(id=profile_id)
        serializer = ProfileSerializer(profile, many=False)
        return Response(serializer.data)
            
    def put(self, request, profile_id):
         profile = Profile.objects.get(id=profile_id)
         profile.address = request.data.get("address")
         profile.birthday = request.data.get("birthday")
         profile.favorite_genre = request.data.get("favorite_genre")
         profile.address = request.data.get("address")
         profile.save()
    
    def delete(self, request, profile_id):
        profile = Profile.objects.get(id=profile_id)
        profile.delete()
        
        return Response(status=status.HTTP_204_NO_CONTENT)
        
class LibraryView(APIView):
    def get(self,request, profile_id):
        library = Profile.library.objects.get(id=profile_id)
        serializer = ProfileSerializer(library, many=true)
        return Response(serializer.data)
        
        

        
 #class TradesView(APIView):
#     def get(self, request, profile_id):
#         trader = Trades.objects.get(profile=profile_id)
#         trades = [ in Trades.objects.all()]
        
        
    def put(self, request, profile_id):
        trade = Trades.objects.get(id=profile_id)
        trade.is_accepted = request.data.get("is_accepted")
        trade.save()
        
        serializer = TradesSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.data, status=status.HTTP_400_BAD_REQUEST)
            
    
    def delete(self, request, profile_id):
        trade = Trades.objects.get(id=profile_id)
        trade.delete()
        
        return Response(status=status.HTTP_204_NO_CONTENT)
        