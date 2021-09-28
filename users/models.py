import uuid
from django.db import models
from django.db.models import Q
from django.db.models.deletion import CASCADE
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError
from django.db.models.signals import post_save
from django.dispatch import receiver

from products.models import Product, ProductType


class Customer(AbstractUser):
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$', 
            message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")
    username = models.CharField(validators=[phone_regex], max_length=17, blank=False, unique=True)

    REQUIRED_FIELDS = ['first_name', 'last_name',]

    def __str__(self):
        if self.is_superuser:
            return f'admin {self.username}'
        return self.username


@receiver(post_save, sender=Customer)
def customer_save(sender, instance, created, **kwargs):
    if created:
        Cart.objects.create(customer = instance)
        

class OrderItem(models.Model):
    item = models.ForeignKey(Product, on_delete=CASCADE, related_name='item_in_order')
    quantity = models.PositiveSmallIntegerField()
    item_type = models.ForeignKey(ProductType, on_delete=CASCADE, related_name='order_item_type')

    def __str__(self):
        return f"{self.item}  //  {self.item_type}  // Amount: {self.quantity}"

    @classmethod
    def _product_type_list(cls):
        return Product.objects.all().values('pk').query
    
    def clean(self):
        # Raises error in admin panel
        if not self.pk:
            if self.item_type not in self.item.product_type.all():
                raise ValidationError('Item_type is not in this product_types', code='invalid')

    def save(self, *args, **kwargs):
        if self.item_type not in self.item.product_type.all():
            raise ValidationError('Item_type is not in this product_types', code='invalid')
        super(OrderItem, self).save(*args, **kwargs)

class Cart(models.Model):
    unique_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True, verbose_name='Cart ID')
    customer = models.ForeignKey(Customer, on_delete=CASCADE)
    products = models.ManyToManyField(OrderItem, blank=True, related_name='orders_in_cart')
    is_processed = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.customer}  // Processed: {self.is_processed} // {self.unique_id}"

    def processed(self, *args, **kwargs):
        self.is_processed = True
        return super(Cart, self).save(*args, **kwargs)