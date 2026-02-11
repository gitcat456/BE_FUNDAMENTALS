from django.db import models

class Data(models.Model):
    name = models.CharField(max_length=50)
    uni = models.CharField(max_length=50)
    nationality = models.CharField(max_length=30)
    id_number = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f" Id_no: {self.id_number}  {self.name}"
