from django.contrib import admin
# from api.models import Contact
# Register your models here.

from api.models import Books, Profile, Inventory, Trades
admin.site.register(Profile)
admin.site.register(Inventory)
admin.site.register(Trades)
admin.site.register(Books)
