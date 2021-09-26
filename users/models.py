import uuid
from django.db import models
from django.utils import timezone
from django.db.models.deletion import CASCADE
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator

from products.models import Product


class Customer(AbstractUser):
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$', 
            message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")
    username = models.CharField(validators=[phone_regex], max_length=17, blank=False, unique=True)

    REQUIRED_FIELDS = ['first_name', 'last_name',]

    def __str__(self):
        if self.is_superuser:
            return f'admin {self.username}'
        return self.username


class OrderItem(models.Model):
    item = models.ForeignKey(Product, on_delete=CASCADE, related_name='product_item')
    quantity = models.PositiveSmallIntegerField()
    
    def __str__(self):
        return f"{self.item}  // Amount: {self.quantity}"

class Cart(models.Model):
    unique_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True, verbose_name='Cart ID')
    customer = models.ForeignKey(Customer, on_delete=CASCADE)
    products = models.ManyToManyField(OrderItem, blank=True, related_name='orders_in_cart')
    is_processed = models.BooleanField(default=False)
    processing_date = models.DateTimeField()

    def __str__(self):
        return f"{self.customer}  // Processed: {self.is_processed} // {self.unique_id}"

    def processed(self, *args, **kwargs):
        self.is_processed = True
        self.processing_date = timezone.now()
        return super(Cart, self).save(*args, **kwargs)