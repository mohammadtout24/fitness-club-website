from django.contrib import admin

# Register your models here.
from .models import Client,Member,Sport,Reservation,Product,CartItem
# Register your models here.
admin.site.register(Client)
admin.site.register(Member)
admin.site.register(Sport)
admin.site.register(Reservation)
admin.site.register(Product)
admin.site.register(CartItem)

