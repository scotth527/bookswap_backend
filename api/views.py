from django.shortcuts import render
import json
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
# from api.models import Contact, ContactSerializer
from api.models import Books, Profile, Inventory, Trades, User
from api.models import BooksSerializer, ProfileSerializer, InventorySerializer, TradesSerializer
from api.models import TradeProfileSerializer, TradeInventorySerializer, TradesViewSerializer, UserSerializer
# from api.models import WishlistSerializer, InterestedBooks
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from django.contrib.auth import authenticate, login
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema

class BooksView(APIView):
    """
    get:
    Return a list of all books 
    """
    
    permission_classes = (AllowAny,)
    
    @swagger_auto_schema(
        responses={ status.HTTP_200_OK : BooksSerializer(many=True)}
    )
    
    def get(self, request, book_id=None):
        if book_id is not None:
            book = Books.objects.get(id=book_id)
            serializer = BooksSerializer(book, many=False)
            return Response(serializer.data)
        else:
            book = Books.objects.all()
            serializer = BooksSerializer(book, many=True)
            return Response(serializer.data)

class CreateUser(APIView): 
    """
    post: 
    Create a new user
    """
    permission_classes = (AllowAny,)
    
    @swagger_auto_schema(
        request_body=ProfileSerializer,
        responses={
            status.HTTP_200_OK : ProfileSerializer,
            status.HTTP_400_BAD_REQUEST: openapi.Response(description="Missing information")
            }
    )
    
    def post(self,request):
        user = request.data
        serializer = ProfileSerializer(data=user)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class UserRetrieveUpdateAPIView(APIView):
 
    # Allow only authenticated users to access this url
    permission_classes = (IsAuthenticated,)
    serializer_class = UserSerializer
 
    @swagger_auto_schema(
        responses = {status.HTTP_200_OK : UserSerializer(many=True)}
    )
    def get(self, request, *args, **kwargs):
        # serializer to handle turning our `User` object into something that
        # can be JSONified and sent to the client.
        serializer = self.serializer_class(request.user)
 
        return Response(serializer.data, status=status.HTTP_200_OK)
        


class LoginView(APIView):
    """
    get:
    Return information about a particular profile.
    
    post:
    Authenticate user
    """
    
    permission_classes = (AllowAny,)
    
    @swagger_auto_schema(
        responses={ status.HTTP_200_OK : ProfileSerializer(many=False)}
    )
    
    def get(self, request):
        user = request.GET['user']
        
        if user is not None:
            try:
                profile = Profile.objects.get(user=user)
            except Profile.DoesNotExist:
                return Response(status=status.HTTP_404_NOT_FOUND)
            
            serializer = ProfileSerializer(profile, many=False)
            return Response(serializer.data)
        
    
    def post(self, request):
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return Response(status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)

class ProfileView(APIView):
    """
    get:
    Return information about a specific user
    
    put:
    Update user information
    
    patch: 
    Used to update the user's wishlist
    
    delete: 
    Delete user profile
    
    """
    
    permission_classes = (IsAuthenticated,)
    
    @swagger_auto_schema(
        responses={ status.HTTP_200_OK : ProfileSerializer(many=False)}
    )
    
    def get(self, request, profile_id=None):
        if profile_id is None:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        else:
            try:
                profile = Profile.objects.get(id=profile_id)
            except Profile.DoesNotExist:
                return Response(status=status.HTTP_404_NOT_FOUND)
            
            serializer = ProfileSerializer(profile, many=False)
            return Response(serializer.data)
    
    @swagger_auto_schema(
        responses={
        status.HTTP_200_OK : ProfileSerializer,
        status.HTTP_400_BAD_REQUEST : openapi.Response(description="Missing information")
        }
    )   
            

    def put(self, request, profile_id=None):
        if profile_id is None:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        else:
            try:
                profile = Profile.objects.get(id=profile_id)
            except Profile.DoesNotExist:
                return Response(status=status.HTTP_404_NOT_FOUND)
                
            profile.address = request.data.get("address")
            profile.birthday = request.data.get("birthday")
            profile.favorite_genre = request.data.get("favorite_genre")
            profile.address = request.data.get("address")
            profile.save()
            return Response(status=status.HTTP_200_OK)
    
    @swagger_auto_schema(
        responses={
        status.HTTP_200_OK : ProfileSerializer,
        status.HTTP_400_BAD_REQUEST : openapi.Response(description="Missing information")
        }
    )   
    
    def patch(self, request, profile_id=None):
        if profile_id is None:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        else:
            try:
                profile = Profile.objects.get(id=profile_id)
            except Profile.DoesNotExist:
                return Response(status=status.HTTP_404_NOT_FOUND)
                
            serializer = ProfileSerializer(profile, data=request.data, partial=True)
            
            if serializer.is_valid():
                serializer.save()
                return Response(status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @swagger_auto_schema(
        response={status.HTTP_204_NO_CONTENT}
        )
        
    def delete(self, request, profile_id=None):
        if profile_id is None:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        else:
            try:
                profile = Profile.objects.get(id=profile_id)
            except Profile.DoesNotExist:
                return Response(status=status.HTTP_404_NOT_FOUND)
                
            profile.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        
        
class LibraryView(APIView):
    
    """
    get:
    Return the inventory of the user
    
    delete: 
    Remove a book from the users inventory
    
    post:
    Add a book to the users inventory
    
    """
    permission_classes = (IsAuthenticated,)
    
    @swagger_auto_schema(
        responses={ status.HTTP_200_OK : TradeInventorySerializer(many=True)}
    )
    
    def get(self, request, profile_id=None):
        if profile_id is None:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        else:
            try:
                library = Inventory.objects.filter(profile=profile_id)
            except Inventory.DoesNotExist:
                return Response(status=status.HTTP_404_NOT_FOUND)
                
            serializer = TradeInventorySerializer(library, many=True)
            return Response(serializer.data)
    
    @swagger_auto_schema(
        response={status.HTTP_204_NO_CONTENT}
        )
            
    def delete(self, request, profile_id=None):
        if profile_id is None:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        else:
            try:
                inventory = Inventory.objects.get(id=profile_id)
            except Inventory.DoesNotExist:
                return Response(Status=status.HTTP_404_NOT_FOUND)
            
            inventory.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
    
    @swagger_auto_schema(
        request_body=InventorySerializer,
        responses={
            status.HTTP_200_OK : InventorySerializer,
            status.HTTP_400_BAD_REQUEST: openapi.Response(description="Missing information")
            }
        )
            
    def post(self, request):
        serializer = InventorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        

class PageView(APIView):   
    
    """
    get: 
    Return information about users who own the book_id 
    
    """
    
    permission_classes = (IsAuthenticated,)
    
    @swagger_auto_schema(
        responses={ status.HTTP_200_OK : TradeProfileSerializer(many=True)}
    )
    
    def get(self, request, book_id=None):
        if book_id is None:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        else:
            try:
                owners = Profile.objects.filter(library__exact=book_id)
            except Profile.DoesNotExist:
                return Response(status=status.HTTP_404_NOT_FOUND)
                
        if owners is not None:
            serializer = TradeProfileSerializer(owners, many=True)
            return Response(serializer.data)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)


class WishersView(APIView):
    
    """
    get:
    Return information on users who have the specified book on their wishlist
    """
    
    permission_classes = (IsAuthenticated,)
    
    @swagger_auto_schema(
        responses={ status.HTTP_200_OK : TradeProfileSerializer(many=True)}
    )
    
    def get(self, request, book_id=None):
        if book_id is None:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        else:
            try:
                wishers = Profile.objects.filter(wishlist__exact=book_id)
            except Profile.DoesNotExist:
                return Response(status=status.HTTP_404_NOT_FOUND)
                
        if wishers is not None:
            serializer = TradeProfileSerializer(wishers, many=True)
            return Response(serializer.data)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)

  
class InventoryView(APIView):
    
    def get(self, request, book_id=None, profile_id=None):
        if book_id is None or profile_id is None:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        else:
            try:
                owned_book = Inventory.objects.get(book=book_id, profile=profile_id)
            except Inventory.DoesNotExist:
                return Response(status=status.HTTP_404_NOT_FOUND)
                
            serializer = InventorySerializer(owned_book, many=False)
            return Response(serializer.data)
            
    
# class WishlistView(APIVIew):
#     serializer_class = ProfileSerializer
    
    
    #partial=true
        
# class WishlistView(APIView):
#     serializer_class = WishlistSerializer
    
#     def get(self, request, profile_id):
#         wishlist = InterestedBooks.objects.filter(profile=profile_id)
#         serializer = WishlistSerializer(wishlist, many=True)
#         return Response(serializer.data)
        
        
class TradesView(APIView):
    """
    get: 
    Return information about the trades for a given user.
    
    patch: 
    Switches is_accepted status between true or false, thus rejecting or 
    accepting trade.
    
    post:
    Submit a new trade request.
    
    delete:
    Cancels a trade.
    """
    
    permission_classes = (IsAuthenticated,)
    
    serializer_class = TradesSerializer
    
    
    
    @swagger_auto_schema(
        responses={ status.HTTP_200_OK : TradesViewSerializer(many=True)}
    )
    
    def get(self, request, given_id):
        user_books = Trades.objects.filter(trader__profile=given_id)
        trades = TradesViewSerializer(user_books, many=True)
        return Response(trades.data)
        
    @swagger_auto_schema(
        responses={
        status.HTTP_200_OK : TradesSerializer,
        status.HTTP_400_BAD_REQUEST : openapi.Response(description="Missing information")
        }
    )   
        
    def patch(self, request, given_id):
        if given_id is None:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        else:
            try:
                trade = Trades.objects.get(id=given_id)
            except Trades.DoesNotExist:
                return Response(status=status.HTTP_404_NOT_FOUND)
                
            serializer = TradesSerializer(trade, data=request.data, partial=True)
            
            if serializer.is_valid():
                serializer.save()
                return Response(status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @swagger_auto_schema(
        request_body=TradesSerializer,
        responses={
            status.HTTP_200_OK : TradesSerializer,
            status.HTTP_400_BAD_REQUEST: openapi.Response(description="Missing information")
            }
        )
    
    def post(self, request):
        serializer = TradesSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
     
    @swagger_auto_schema(
        response={status.HTTP_204_NO_CONTENT}
        ) 
            
    def delete(self, request, given_id):
        trade = Trades.objects.get(id=given_id)
        trade.delete()
        
        return Response(status=status.HTTP_204_NO_CONTENT)

        
class RequestsView(APIView):
    
    """
    get:
    Return a list of trades from the receiver's perspective.
    
    put: 
    Accept or decline the trade by updating the status of the trade. 
    
    delete: 
    Delete the trade. 
    """
    
    permission_classes = (IsAuthenticated,)
    
    @swagger_auto_schema(
        responses={ status.HTTP_200_OK : TradesSerializer(many=True)}
    )
    
    def get(self, request, given_id):
        user_books = Trades.objects.filter(receiver__profile=given_id)
        trades = TradesSerializer(user_books, many=True)
        return Response(trades.data)
    
    @swagger_auto_schema(
        responses={
        status.HTTP_200_OK : TradesSerializer,
        status.HTTP_400_BAD_REQUEST : openapi.Response(description="Missing information")
        }
    )   
        
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
    
    @swagger_auto_schema(
        response={status.HTTP_204_NO_CONTENT}
        )       
    
    def delete(self, request, profile_id):
        trade = Trades.objects.get(id=profile_id)
        trade.delete()
        
        return Response(status=status.HTTP_204_NO_CONTENT)
        