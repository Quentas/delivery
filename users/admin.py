from django.contrib import admin
from .models import Customer, Cart, OrderItem

admin.site.register(Customer)
admin.site.register(Cart)
admin.site.register(OrderItem)

