from django.urls import path, include
from .views import list_create_data, data_detail, DataViewSets
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'model-view-set', DataViewSets)


urlpatterns = [
    path('viewsets/', include(router.urls)),
    path('data_list/', list_create_data),
    path('data_detail/<uuid:uuid>/', data_detail),
    
]