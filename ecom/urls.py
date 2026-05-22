from django.urls import path, include
from .views import order_list, order_create, ProductViewset, OrderViewSet, order_detail
from rest_framework.routers import DefaultRouter
from . import views

router=DefaultRouter()
router.register(r'products', ProductViewset)
router.register(r'orders', OrderViewSet)

urlpatterns = [
    
    #orders
    path('orders/', order_list),
    path('orders/create/', order_create),
    path('order_detail/<int:pk>/', order_detail),
    path('orders/<int:order_id>/attachment/', views.upload_order_attachment_view),
    path('', include(router.urls)),
    
     # products
    path('products/', ProductViewset.as_view({'get': 'list', 'post': 'create'})),
    path('products/<int:pk>/', ProductViewset.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'})),
    path('products/<int:product_id>/image/', views.upload_product_image_view),

    
]