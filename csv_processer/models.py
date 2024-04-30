from django.db import models


# Create your models here.
class UploadedCSV(models.Model):
    Name = models.CharField(max_length=64)
    Class = models.CharField(max_length=64)
    School = models.CharField(max_length=64)
    State = models.CharField(max_length=64)
    upload_date = models.DateTimeField(auto_now_add=True)
