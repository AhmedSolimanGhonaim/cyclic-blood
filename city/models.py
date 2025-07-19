from django.db import models

# Create your models here.

from django.contrib.gis.db import models as geomodels


class City (models.Model):
    name = models.CharField(max_length=40, null=True, blank=True)
    location = geomodels.PointField(geography=True)

    def __str__(self):
        return f'city is {self.name} '

