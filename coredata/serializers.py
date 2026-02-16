from rest_framework import serializers
from .models import Data
import re

class DataSerializer(serializers.ModelSerializer):
    
     class Meta:
        model = Data
        fields = ['id', 'name', 'uni', 'nationality', 'id_number']
        
        #field level validation
     def validate_id_number(self, value):
        if len(str(value)) < 5 or value < 0 :
            raise serializers.ValidationError("ID number must be at least 5 digits and positive")
        return value
    
     def validate_name(self, value):
        value = value.strip() #prevent empty strings or weird spacing:

        if not re.fullmatch(r"[A-Za-z\s'-]+", value): #reject numbers 
            raise serializers.ValidationError(
                "Name must contain only letters, spaces, hyphens or apostrophes."
            )
        return value
    
        #Object-Level validation
     def validate(self, data):
         if data['uni'].lower() == "mku" and data['nationality'].lower() != "kenya":
             raise serializers.ValidationError(
                 f"only Kenyans can be enrolled in MKU!! \n please check for unis available for {data['nationality']} students"
                 
             )
         return data
         
        
    # id = serializers.IntegerField(read_only=True) #read_only because DB creates it.
    # name = serializers.CharField(max_length=50)
    # uni = serializers.CharField(max_length=50)
    # nationality = serializers.CharField(max_length=30)
    # id_number = serializers.IntegerField()
    # created_at = serializers.DateTimeField(read_only=True) #bcoz auto genereated
    # uuid = serializers.UUIDField(read_only=True) # model sets it automatically

    # def create(self, validated_data):
    #     return Data.objects.create(**validated_data)
    
    # #works when :serializer = DataSerializer(instance=obj, data=request_data)
    # def update(self, instance, validated_data):
    #     instance.name = validated_data.get("name", instance.name) #take the new value if the client provided it, Otherwise, keep the old value (instance.name) Then assign it to instance.name.
    #     instance.uni = validated_data.get("uni", instance.uni)
    #     instance.nationality = validated_data.get("nationality", instance.nationality)
    #     instance.id_number = validated_data.get("id_number", instance.id_number)
    #     instance.save() #Persists changes to the database.
    #     return instance  #Returns the updated object, which DRF will use for serialization back to JSON.
    
    # #serailization ie Model->JSON
    # #called when you access : serializer = DataSerializer(obj)
    # def to_representation(self, instance):
    #     print("REPRESENTING")
    #     return super().to_representation(instance) #Converts instance fields into a Python dictionary that becomes JSON.
    
    # #deserialization ie JSON-> Python
    # #called when : serializer = DataSerializer(data=request_data)
    # def to_internal_value(self, data):
    #     print("PROCESSING INPUT")
    #     return super().to_internal_value(data)



   