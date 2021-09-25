from django.shortcuts import render
from .serializers import *
from .models import *

from django.views import View
from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect, JsonResponse

from rest_framework.viewsets import ViewSet, ModelViewSet
from rest_framework.response import Response
from rest_framework.permissions import (
    IsAuthenticated,
    AllowAny,
)

class CartViewSet(ViewSet):
    
    def list(self, request):
        queryset = Cart.objects.get(customer__id = 1)
        serializer = CartSerializer(queryset, many=False)
        return Response(serializer.data)