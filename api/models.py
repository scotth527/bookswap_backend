from rest_framework import serializers
from django.db import models
from django.conf import settings

# Create your models here. 
    
class Profile(models.Model):
    address = models.CharField(max_length=50)
    birthday = models.CharField(max_length=50)
    favorite_genre = models.CharField(max_length=50)
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    
class Books(models.Model):
    Goodreads_ID = models.CharField(max_length=50)
    ID = models.CharField(max_length=50)
    Title = models.CharField(max_length=50)
    Author = models.CharField(max_length=50)
    Genre = models.CharField(max_length=50)
    Language = models.CharField(max_length=50)
    Description = models.CharField(max_length=1000)

    
class Wishlist(models.Model):
    book_id = models.ForeignKey('Books', on_delete=models.CASCADE)


class PersonalInventory(models.Model):
    book_id = models.ForeignKey('Books', on_delete=models.CASCADE)
    
        
class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        exclude = ()
        
class WishlistSerializer(serializers.ModelSerializer):
    class Meta: 
        model = Wishlist
        exclude = ()
        
class PersonalInventorySerializer(serializers.ModelSerializer):
    class Meta:
        model = PersonalInventory
        exclude = ()
        
class BooksSerializer(serializers.ModelSerializer):
    class Meta:
        model = Books
        exclude = ()
        
        