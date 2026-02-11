from django.db import models
import uuid 

class Data(models.Model):
    name = models.CharField(max_length=50)
    uni = models.CharField(max_length=50)
    nationality = models.CharField(max_length=30)
    id_number = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, blank=True, null=True)
    
    def __str__(self):
        return f" Id_no: {self.id_number}  {self.name}"
