from rest_framework import serializers
from django.db import models
from django.conf import settings

# Create your models here. 
class Books(models.Model):
    api_id = models.CharField(max_length=50)
    title = models.CharField(max_length=50)
    author = models.CharField(max_length=50)
    genre = models.CharField(max_length=50)
    language = models.CharField(max_length=50)
    description = models.CharField(max_length=1000)
    image = models.CharField(max_length=1000, default="https://images.gr-assets.com/books/1388190055l/10048834.jpg")
    

class Profile(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    address = models.CharField(max_length=50)
    birthday = models.DateField(auto_now=False, auto_now_add=False)
    favorite_genre = models.CharField(max_length=50)
    library = models.ManyToManyField(
        Books,
        blank=True,
        related_name="owners",
        through='Inventory',
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

   
# class Wishlist(models.Model):
#     book_id = models.ForeignKey('Books', on_delete=models.CASCADE)

# # class InterestedBooks(models.Model):
#     book = models.ForeignKey(Books, on_delete=models.CASCADE)
#     profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    
    
class Inventory(models.Model):
    book = models.ForeignKey(Books, on_delete=models.CASCADE)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    status = models.BooleanField(default=True)

class Trades(models.Model):
    trader = models.ForeignKey(Inventory, on_delete=models.CASCADE, related_name="trader")
    requester = models.ForeignKey(Inventory, on_delete=models.CASCADE, related_name="requester")
    is_accepted = models.BooleanField(default=False)




class ProfileSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Profile
        exclude = ()

class InventorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Inventory
        exclude = ()
      
class TradesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Trades
        exclude = ()
        
        
# class WishlistSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = InterestedBooks
#         exclude = ()
# class WishlistSerializer(serializers.ModelSerializer):
#     class Meta: 
#         model = Wishlist
#         exclude = ()
        
# class PersonalInventorySerializer(serializers.ModelSerializer):
#     class Meta:
#         model = PersonalInventory
#         exclude = ()
        
class BooksSerializer(serializers.ModelSerializer):
    class Meta:
        model = Books
        exclude = ()
        
        