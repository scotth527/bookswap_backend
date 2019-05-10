from rest_framework import serializers, status
from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from drf_yasg import openapi
import json
from django.shortcuts import render
from rest_framework import status, generics
from rest_framework.views import APIView
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
from django.contrib.auth.hashers import make_password

# Create your models here. 
GENRE_CHOICES = (
    ('Science Fiction', 'Science Fiction'),
    ('Biography', 'Biography'),
    ('Classics', 'Classics'),
    ('Horror', 'Horror'),
    ('Comedy', 'Comedy'),
    ('Fantasy', 'Fantasy'),
    ('Romance', 'Romance'),
) 
class Books(models.Model):
    ENGLISH = 'EN'
    SPANISH = 'SP'
    FRENCH = 'FR'
    CHINESE = 'CH'
    JAPANESE = 'JP'
    KOREAN = 'KN'
    ARABIC = 'AR'
    LANGUAGE_CHOICES = (
        (ENGLISH, 'English'),
        (SPANISH, 'Spanish'),
        (FRENCH, 'French'),
        (CHINESE, 'Chinese'),
        (JAPANESE, 'Japanese'),
        (KOREAN, 'Korean'),
        (ARABIC, 'Arabic'),
    )
 
    api_id = models.CharField(max_length=50)
    title = models.CharField(max_length=50)
    author = models.CharField(max_length=50)
    genre = models.CharField(max_length=50,
        choices=GENRE_CHOICES,
        default='Fantasy',)
    language = models.CharField(max_length=2,
        choices=LANGUAGE_CHOICES,
        default=ENGLISH,)
    description = models.CharField(max_length=1000)
    image = models.CharField(max_length=1000, default="https://images.gr-assets.com/books/1388190055l/10048834.jpg")
    thumbnail = models.CharField(max_length=1000, default="https://vinniefisher.com/wp-content/uploads/2016/07/CEOMindset-Book-Thumbnail-Listings.png")
    class Meta: 
        verbose_name_plural = "Books"
    

class Profile(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    address = models.CharField(max_length=50)
    city = models.CharField(max_length=50, default="Miami")
    state = models.CharField(max_length=50, default="FL")
    birthday = models.DateField(auto_now=False, auto_now_add=False)
    favorite_genre = models.CharField(max_length=50,
        choices=GENRE_CHOICES,
        default='Fantasy',)
    library = models.ManyToManyField(
        Books,
        blank=True,
        related_name="owners",
        through='Inventory'
    )
    wishlist = models.ManyToManyField(
        Books,
        blank=True,
        # related_name="wanted_books",
        # through='InterestedBooks',
    )
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    

          
class BooksSerializer(serializers.ModelSerializer):
    class Meta:
        model = Books
        exclude = ()
        
    
class Inventory(models.Model):
    book = models.ForeignKey(Books, on_delete=models.CASCADE)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    status = models.BooleanField(default=True)

class Trades(models.Model):
    trader = models.ForeignKey(Inventory, on_delete=models.CASCADE, related_name="trader")
    requester = models.ForeignKey(Inventory, on_delete=models.CASCADE, related_name="requester")
    is_accepted = models.BooleanField(default=False)
    class Meta: 
        verbose_name_plural = "Trades"


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'id')
        extra_kwargs = {"password":
                            {"write_only":True}
                            }
        
        
class ProfileSerializer(serializers.ModelSerializer):
    wishlist = serializers.PrimaryKeyRelatedField(many=True, read_only=False, queryset=Books.objects.all())
    user=UserSerializer(required=True)
    class Meta:
        model = Profile
        exclude = ()
        
    def create(self, validated_data):

        user = User.objects.create_user(**validated_data.pop('user'))
        profile, created = Profile.objects.update_or_create(user=user, 
            first_name=validated_data.pop('first_name'), 
            last_name=validated_data.pop('last_name'), address=validated_data.pop('address'), 
            city=validated_data.pop('city'), state=validated_data.pop('state'), 
            birthday=validated_data.pop('birthday'), 
            favorite_genre=validated_data.pop('favorite_genre'), 
        )
        return profile
        

class TradeProfileSerializer(serializers.ModelSerializer):
    user=UserSerializer()
    wishlist = serializers.PrimaryKeyRelatedField(many=True, read_only=False, queryset=Books.objects.all())
    
    class Meta:
        model = Profile
        exclude = ()
        

class InventorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Inventory
        exclude = ()
        

class TradeInventorySerializer(serializers.ModelSerializer):
    book = BooksSerializer()

    
    class Meta:
        model = Inventory
        exclude = ()

        
        
class TradeViewInventorySerializer(serializers.ModelSerializer):
    book = BooksSerializer()
    profile = TradeProfileSerializer()
    
    class Meta:
        model = Inventory
        exclude = ()        
      
class TradesSerializer(serializers.ModelSerializer):
    # trader = TradeInventorySerializer()
    # requester = TradeInventorySerializer()
    
    # trader__profile = TradeProfileSerializer()
    
    class Meta:
        model = Trades
        exclude = ()
        

class TradesViewSerializer(serializers.ModelSerializer):
    trader = TradeViewInventorySerializer()
    requester = TradeViewInventorySerializer()
    
    class Meta:
        model = Trades
        exclude = () 
 
        
        