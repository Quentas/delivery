from django.urls import path

from .views import CartViewSet


urlpatterns = [
    path('cart/', CartViewSet.as_view({
        'get' : 'list',
    })),
]
