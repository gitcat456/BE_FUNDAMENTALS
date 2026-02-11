from django.urls import path
from .views import list_data

urlpatterns = [
    path('data_list/', list_data)
]