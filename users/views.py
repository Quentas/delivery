from django.shortcuts import render
from .serializers import *
from .models import *
from django.db.models import Q
from django.views import View
from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect, JsonResponse
from django.db import transaction
from rest_framework.viewsets import ViewSet, ModelViewSet
from rest_framework.response import Response
from rest_framework.permissions import (
    IsAuthenticated,
    AllowAny,
)

class CartViewSet(ViewSet):
    permission_classes = (IsAuthenticated,)
    
    def list(self, request):
        '''Returns current user cart. If none, creates one
        '''
        queryset, created = Cart.objects.filter(
            Q (is_processed = False)).get_or_create(customer = request.user)
        serializer = CartSerializer(queryset, many=False)
        return Response(serializer.data)

    @transaction.atomic
    def add_to_cart(self, request):
        '''Adds items to cart
        '''
        user_cart = Cart.objects.filter(customer = request.user).order_by('-id')[0]
        item_id = int(request.data['id'])
        product = get_object_or_404(Product, id=item_id)
        quantity = int(request.data['quantity'])
        #product_type = request.data['type']
        
        # Checks if this order item is already in cart. If so, increases its quantity by incoming quantity
        # Otherwise adds this product as new OrderItem
        if item_id in [x.item.id for x in user_cart.products.all()]:
            increase_quantity_in = user_cart.products.get(item__id=item_id)
            increase_quantity_in.quantity = increase_quantity_in.quantity + quantity
            increase_quantity_in.save()
        else:
            orderitem = OrderItem.objects.create(item = product, quantity = quantity)
            user_cart.products.add(orderitem)
            user_cart.save()

        return Response(status=200)

    def remove_from_cart(self, request):
        '''Removes items from cart
        '''


        queryset, created = Cart.objects.filter(
            Q (is_processed = False)).get(customer = request.user)
        
        pass

    def delete(self, request):
        '''Completely removes cart
        '''
        pass

    def process(self, request):
        '''Sends cart to processing. If successful, marks as 
            'is_processed=True' and creates new empty cart
        '''
        pass