from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator 

class Auto(models.Model):
    znacka = models.CharField(max_length = 50)
    model = models.CharField(max_length = 200)
    rok_vyroby = models.IntegerField(validators=[MinValueValidator(1880), MaxValueValidator(2050)])
