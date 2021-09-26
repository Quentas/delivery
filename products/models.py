import products
from django.db import models
from django.db.models.deletion import CASCADE, DO_NOTHING

class ProductType(models.Model):
    weight = models.IntegerField(blank=False)
    price = models.IntegerField(blank=False)

    def __str__(self) -> str:
        return f"Weight: {self.weight}   //   Price: {self.price}"

class Category(models.Model):
    name = models.CharField(blank=False, max_length=50)
    photo =  models.TextField(blank=False, max_length=500)

    class Meta:
        verbose_name_plural = "Categories"
    
    def __str__(self) -> str:
        return self.name

    def save(self, *args, **kwargs):
        self.name = self.name.lower()
        super(Category, self).save(*args, **kwargs)

class Manufacturer(models.Model):
    name = models.CharField(blank=False, max_length=50)

    class Meta:
        verbose_name_plural = "Manufacturers"
    
    def __str__(self) -> str:
        return self.name


class Product(models.Model):
    name = models.CharField(blank=False, max_length=50)
    description = models.TextField(blank=False, max_length=300)
    discount = models.PositiveSmallIntegerField(blank=True, verbose_name='Discount, in %', default=0)
    manufacturer = models.ForeignKey(Manufacturer, on_delete=DO_NOTHING, blank=False)
    category = models.ForeignKey(Category, on_delete=DO_NOTHING, blank=False)
    photo = models.TextField(blank=False, max_length=500)
    product_type = models.ManyToManyField(ProductType, blank=False, symmetrical=False)

    def __str__(self) -> str:
        return f"{self.name} // {self.category} // by {self.manufacturer}"

    def save(self, *args, **kwargs):
        if self.discount in range(0, 101):
            return super(Product, self).save(*args, **kwargs)
