from django.db import models

# Create your models here.
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
 ROLE_CHOICES = (
     ('donor', 'Donor'),
     ('hospital', 'Hospital'),
     ('admin', 'Admin'),
 )
 role = models.CharField(max_length=20, choices=ROLE_CHOICES)
 city = models.CharField(max_length=100, blank=True,null=True)
