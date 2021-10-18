from django.shortcuts import render
from .serializers import *
from .models import *
from django.db.models import Q
from django.shortcuts import get_object_or_404
from django.db import transaction
from rest_framework.viewsets import ViewSet, ModelViewSet
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.response import Response
from django.http import JsonResponse
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
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
        '''Adds items to cart, if 'quantity' parameter is positive.
            Otherwise removes it from cart
        '''
        user_cart = Cart.objects.filter(customer = request.user).order_by('-id')[0]
        item_id = int(request.data['id'])
        product = get_object_or_404(Product, id=item_id)
        quantity = int(request.data['quantity'])
        item_type = int(request.data['type']) # receives only 'weight' of the product
        item_type = get_object_or_404(product.product_type.all(), weight=item_type)

        # Checks if this order item is already in cart. If so, increases its quantity by incoming quantity
        # Otherwise adds this product as new OrderItem
        if (
            item_id in [x.item.id for x in user_cart.products.all()] and 
            item_type in [y.item_type for y in user_cart.products.all()]
            ):
            increase_quantity_here = user_cart.products.get(item__id=item_id, item_type=item_type)
            increase_quantity_here.quantity = increase_quantity_here.quantity + quantity
            increase_quantity_here.save()
        else:
            orderitem = OrderItem.objects.create(item=product, quantity=quantity, item_type=item_type)
            user_cart.products.add(orderitem)
            user_cart.save()

        return Response(status=200)

    @transaction.atomic
    def delete(self, request):
        '''Completely removes cart and all linked orderItems and creates new empty cart
        '''
        response = 1
        try:
            user_cart = Cart.objects.get(customer=request.user, is_processed=False)
            for item in user_cart.products.all():
                item.delete()            
            user_cart.delete()
            Cart.objects.create(customer=request.user)
            response = Response({'deleting':'Delete success. Created new cart for this user'}, status=200)    
        except ObjectDoesNotExist:
            Cart.objects.create(customer=request.user)
            response = Response(status=204)
        return response

    @transaction.atomic
    def process(self, request):
        '''Sends cart to processing. If successful, marks as 
            'is_processed=True' and creates new empty cart
        '''
        final_price = 0
        user_cart = Cart.objects.get(customer=request.user, is_processed=False)
        if user_cart.products.all().count() == 0:
            return Response({'processing_error': 'Your cart is empty'}, status=400)
        for item in user_cart.products.all():
            item_discount = item.item
            item_discount = item_discount.discount
            
            item_price = item.item_type
            item_price = item_price.price

            order_item_price = item_price * (1 - (item_discount / 100)) * item.quantity

            final_price = final_price + order_item_price
        user_cart.processed()
        
        return Response({'final_price': final_price}, status=200)

    def previous_carts(self, request):
        '''Returns all previous carts of a current user
        '''
        queryset = Cart.objects.filter(
            customer=request.user, is_processed=True
        ).order_by('-id')
        serializer = PreviousCartListSerializer(queryset, many=True)
        return Response(serializer.data)

    def preview_previous_cart(self, request, uid):
        '''Previews previous cart with its processing date
        '''
        user_cart = get_object_or_404(Cart, unique_id=uid)
        if request.user.id is not user_cart.customer.id:
            return Response({'auth_error':'You have no permission to preview this cart'}, status=401)
        return Response(PreviousCartSerializer(user_cart).data)


def ping(request):
    data = {'ping': 'pong!'}
    return JsonResponse(data)
