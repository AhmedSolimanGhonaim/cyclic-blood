from django.db import models

# Create your models here.
from django.contrib.auth.models import AbstractUser

from django.contrib.gis.db import models as geomodels
from city.models import City


class CustomUser(AbstractUser):
    ROLE_CHOICES = (
        ('donor', 'Donor'),
        ('hospital', 'Hospital'),  
        ('bank_employee', 'Blood Bank'),
    )
    
    email = models.EmailField(unique=True)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    city = models.ForeignKey(City,on_delete=models.SET_NULL,blank=True,null=True)
    location =geomodels.PointField(geography=True,null=True,blank=True )
    
    
    def save(self, *args,**kwargs):
        if self.city and not self.location:
            self.location = self.city.location
        
        return super().save(*args,**kwargs)
        
    def __str__(self):
        return f"{self.username} - {self.role} - {self.city}"

