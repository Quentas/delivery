from django.contrib import admin
from .models import (
    Product,
    Category,
    Manufacturer,
    ProductType,
)

from django.contrib.auth.models import Group
admin.site.register(Manufacturer)
admin.site.register(Category)
admin.site.register(ProductType)
admin.site.register(Product)
admin.site.unregister(Group)