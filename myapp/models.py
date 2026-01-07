from django.db import models

# Create your models here.
# models.py
from django.db import models

class DailyChart(models.Model):
    station_name = models.CharField(max_length=200)
    station_id = models.CharField(max_length=100)
    station_code = models.CharField(max_length=100)
    assignment = models.CharField(max_length=200)
    date = models.DateField()
    image = models.ImageField(upload_to='daily-charts/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.station_name
