from django.urls import path

from .views import ProductViewSet, CategotyViewSet


urlpatterns = [
    path('list/<category>', ProductViewSet.as_view({
        'get' : 'list',
    })),
    path('cat_list/', CategotyViewSet.as_view({
        'get' : 'get_categories',
    })),

]
