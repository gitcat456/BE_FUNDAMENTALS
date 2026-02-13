from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import Data
from .serializers import DataSerializer
from django.shortcuts import get_object_or_404
from rest_framework import viewsets 


class DataViewSets(viewsets.ModelViewSet):
    queryset = Data.objects.all()
    serializer_class = DataSerializer

#tell DRF that this is an API endpoint 
@api_view(["GET", "POST"]) #Error 405-method not allowed for other methods 
def list_create_data(request):
    
  if request.method == "GET":
    queryset = Data.objects.all()
    
    #take python objects and convert them into JSON-safe data
    #many=True coz a queryset is not a single object
    serializer = DataSerializer(queryset, many=True)
    
    #serializer.data->python dict/list Response converts to Json
    return Response(serializer.data)
  
  elif request.method == "POST":
      #take this raw input and validate it against the Data model
      serializer = DataSerializer(data=request.data)
      if serializer.is_valid():
          #create a data instance
          serializer.save()
          print(serializer.data)
          return Response(serializer.data, status=201)
      #failure response
      return Response(serializer.errors, status=400)
  
@api_view(["GET", "PATCH", "DELETE"])
def data_detail(request, uuid):
    #obj = Data.objects.get(uuid=uuid)
    obj = get_object_or_404(Data, uuid=uuid)
    
    if request.method == "GET":
        serializer = DataSerializer(obj)
        return Response(serializer.data)
    
    elif request.method == "PATCH":
        serializer = DataSerializer(obj, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data , status=200)
        return Response(serializer.errors, status=400)
    
    elif request.method == "Delete":
        obj.delete()
        return Response(status=204)
        