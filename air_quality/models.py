from django.db import models


# Create your models here.
AIR_QUALITY = []

class Air_quality(models.Model):
    id = models.IntegerField(primary_key=True)
    date = models.DateField()
    pm25 = models.FloatField(default = 1.0)
    pm10 = models.FloatField(default=1.0)
    temp = models.FloatField(default=1.0)
    aqi = models.FloatField(default=1.0)
    