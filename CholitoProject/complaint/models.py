import datetime as datetime

import django
from django.db import models

from municipality.models import Municipality


class AnimalType(models.Model):
    name = models.TextField(max_length=100)

    def __str__(self):
        return self.name


class Complaint(models.Model):
    COMPLAINT_OPTIONS = (
        (1, "Abandono en la calle"),
        (2, "Exposicion a temperaturas<br>extremas"),
        (3, "Falta de agua"),
        (4, "Falta de comida"),
        (5, "Violencia"),
        (6, "Venta ambulante"),
    )

    COMPLAINT_STATUS = (
        (1, "Reportada"),
        (2, "Consolidada"),
        (3, "Verificada"),
        (4, "Cerrada"),
        (5, "Desechada"),
    )

    GENDER_OPTIONS = (
        (1, "Macho"),
        (2, "Hembra"),
    )

    WOUND_OPTIONS = (
        (True, "Sí"),
        (False, "No"),
    )

    description = models.TextField(max_length=1000)
    case = models.SmallIntegerField(choices=COMPLAINT_OPTIONS)
    lat = models.DecimalField(max_digits=13, decimal_places=10, null=True)
    lng = models.DecimalField(max_digits=13, decimal_places=10, null=True)
    directions = models.TextField(max_length=200, null=True)
    status = models.SmallIntegerField(choices=COMPLAINT_STATUS)
    animal_type = models.ForeignKey(AnimalType)
    gender = models.SmallIntegerField(choices=GENDER_OPTIONS)
    wounded = models.BooleanField(choices=WOUND_OPTIONS)
    color = models.TextField(max_length=50)
    datetime = models.DateTimeField(auto_now_add=True, null=False, blank=False)
    # The next line is only for testing purposes
    #datetime.editable = True
    municipality = models.ForeignKey(Municipality)

    def __str__(self):
        return "Complaint #" + str(self.pk)


class ComplaintImage(models.Model):
    image = models.ImageField(upload_to='complaints/')
    complaint = models.ForeignKey('Complaint', on_delete=models.CASCADE)
