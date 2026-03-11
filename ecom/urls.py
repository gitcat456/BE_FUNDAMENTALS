from django.urls import path, include
from .views import order_list, order_create, ProductViewset
from rest_framework.routers import DefaultRouter

router=DefaultRouter()
router.register(r'products', ProductViewset)

urlpatterns = [
    path('orders/', order_list),
    path('order_create/', order_create),
     path('', include(router.urls)),
]