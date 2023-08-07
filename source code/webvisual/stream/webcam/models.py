from django.db import models

# Create your models here.
class DataCam(models.Model):
    Id = models.CharField(primary_key=True,max_length=50,null = False)
    name = models.CharField(max_length=50,null = False)

    def __str__(self):
        return f"{self.Id},{self.name}"