from rest_framework import serializers
from .models import Data

class DataSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True) #read_only because DB creates it.
    name = serializers.CharField(max_length=50)
    uni = serializers.CharField(max_length=50)
    nationality = serializers.CharField(max_length=30)
    id_number = serializers.IntegerField()
    created_at = serializers.DateTimeField(read_only=True) #bcoz auto genereated
    uuid = serializers.UUIDField(read_only=True) # model sets it automatically

    def create(self, validated_data):
        return Data.objects.create(**validated_data)
    
    def update(self, instance, validated_data):
        instance.name = validated_data.get("name", instance.name)
        instance.uni = validated_data.get("uni", instance.uni)
        instance.nationality = validated_data.get("nationality", instance.nationality)
        instance.id_number = validated_data.get("id_number", instance.id_number)
        instance.save()
        return instance


# class DataSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Data
#         fields = "__all__"
