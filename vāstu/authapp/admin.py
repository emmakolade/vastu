from django.contrib import admin
from .models import User, OwnerUser, BuyerUser

admin.site.register(User)
admin.site.register(OwnerUser)
admin.site.register(BuyerUser)
