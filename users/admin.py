from django.contrib import admin
from .models import Customer, Cart, OrderItem

class CartAdmin(admin.ModelAdmin):
    readonly_fields=('processing_date',)

admin.site.register(Customer)
admin.site.register(Cart, CartAdmin)
admin.site.register(OrderItem)


