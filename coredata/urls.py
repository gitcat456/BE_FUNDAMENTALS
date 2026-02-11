from django.urls import path
from .views import list_data

urlpattern = [
    path('data_list/', list_data)
]