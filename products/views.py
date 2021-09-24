from django.shortcuts import render
from .serializers import *
from .models import Product, Category

from django.views import View
from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect, JsonResponse

from rest_framework.viewsets import ViewSet, ModelViewSet
from rest_framework.response import Response
from rest_framework.permissions import (
    IsAuthenticated,
    AllowAny,
)

from .serializers import ProductSerializer

class ProductViewSet(ViewSet):
    def list(self, request, category):
        self.permission_classes = (AllowAny,)
        categories = [item.name for item in Category.objects.all()]
        if category not in categories and category != 'all':
            return Response(
                {'category_mismatch': 'unable to find products with such category'}, status=400)
        if category == 'all':
            queryset = Product.objects.all()
        else:
            queryset = Product.objects.filter(category__name = category)
        serializer = ProductSerializer(
            queryset.order_by("-id"), many=True, context={'request': request}
            )
        return Response(serializer.data)


class CategotyViewSet(ViewSet):
    
    def get_categories(self, request):
        self.permission_classes = (AllowAny,)
        queryset = Category.objects.all().order_by('name')
        serializer = CategorySerializer(queryset, many=True)
        return Response(serializer.data)