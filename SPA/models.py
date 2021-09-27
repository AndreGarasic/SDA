from django.db import models

# Create your models here

class Taz_model(models.Model):
    taz_id = models.CharField(max_length=100)
    shape = models.CharField(max_length=100)
    sink = models.CharField(max_length=100)
    source = models.CharField(max_length=100)
    weight = models.DecimalField(max_digits=4, decimal_places=3)
    def __str__(self):
        return self.taz_id