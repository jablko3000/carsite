from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator 

class Auto(models.Model):
    znacka = models.CharField(max_length = 50)
    model = models.CharField(max_length = 200)
    rok_vyroby = models.IntegerField(validators=[MinValueValidator(1880), MaxValueValidator(2050)])
    cena = models.IntegerField(validators=[MinValueValidator(0)])
    img = models.CharField(max_length = 200)
    def __str__(self):
        return f"Auto značky {self.znacka}, modelu {self.model}, z roku {self.rok_vyroby}"

class Rezervace(models.Model):
    auto = models.ForeignKey(Auto, on_delete=models.CASCADE)
    datum_a_cas = models.DateTimeField()
    def __str__(self):
        return f"Rezervace pro {self.auto} - {self.datum_a_cas}"
