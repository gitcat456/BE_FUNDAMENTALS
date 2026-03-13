from django.urls import path, include
from .views import order_list, order_create, ProductViewset, OrderViewSet, order_detail
from rest_framework.routers import DefaultRouter

router=DefaultRouter()
router.register(r'products', ProductViewset)
router.register(r'orders', OrderViewSet)

urlpatterns = [
    path('order_list/', order_list),
    path('order_create/', order_create),
    path('order_detail/<int:pk>/', order_detail),
    path('', include(router.urls)),
]