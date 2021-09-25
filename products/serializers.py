import products
from django.db.migrations.operations import fields
from rest_framework.fields import SerializerMethodField
from rest_framework import serializers
from django.shortcuts import get_object_or_404


from .models import (
    Product,
    Manufacturer, 
    Category,
    ProductType,
)

class ProductTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductType
        exclude = ('id',)


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('name', 'photo',)


class ManufacturerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Manufacturer
        fields = (
            'name',
        )

class ProductSerializer(serializers.ModelSerializer):
    manufacturer = ManufacturerSerializer()
    category_name = serializers.CharField(source='category.name')
    product_type = ProductTypeSerializer(many=True)
    class Meta:
        model = Product
        fields = (
            'id', 'name', 'description', 'discount', 'photo',
            'category_name', 'manufacturer', 'product_type',
        )
    