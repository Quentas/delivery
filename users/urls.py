from django.urls import path

from .views import CartViewSet


urlpatterns = [
    path('cart/', CartViewSet.as_view({
        'get' : 'list',
        'post' : 'add_to_cart',
        'delete': 'delete',
    })),
    path('cart/process/', CartViewSet.as_view({
        'post' : 'process',
    })),
    path('cart/list_previous/', CartViewSet.as_view({
        'get' : 'previous_carts',
    })),
    path('cart/<uid>', CartViewSet.as_view({
        'get' : 'preview_previous_cart',
    }))
]
