import products
from django.db.models import fields
from products.serializers import ProductSerializer
from rest_framework import serializers
from .models import OrderItem, Cart, Customer


class OrderItemSerializer(serializers.ModelSerializer):
    item = ProductSerializer()
    class Meta:
        model = OrderItem
        fields = ('item', 'quantity',)


class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = ('phone',)


class CartSerializer(serializers.ModelSerializer):
    customer = CustomerSerializer()
    products = OrderItemSerializer(many=True)
    class Meta:
        model = Cart
        fields = ('customer', 'unique_id', 'products')