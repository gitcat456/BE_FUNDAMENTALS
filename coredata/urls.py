from django.urls import path
from .views import list_create_data, data_detail

urlpatterns = [
    path('data_list/', list_create_data),
    path('data_detail/<uuid:uuid>/', data_detail),
]