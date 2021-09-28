from django.db import models
import products
from django.db.models import fields
from products.serializers import ProductSerializer, ProductTypeSerializer
from rest_framework import serializers
from .models import OrderItem, Cart, Customer


class OrderItemSerializer(serializers.ModelSerializer):
    item = ProductSerializer()
    item_type = ProductTypeSerializer()
    class Meta:
        model = OrderItem
        fields = ('item', 'quantity', 'item_type',)


class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = ('username',)


class CartSerializer(serializers.ModelSerializer):
    customer = CustomerSerializer()
    products = OrderItemSerializer(many=True)
    class Meta:
        model = Cart
        fields = ('customer', 'unique_id', 'products')


class ProcessedCartSerializer(CartSerializer):
    class Meta:
        model = Cart
        fields = CartSerializer.Meta.fields + ('is_processed', 'processing_date',)