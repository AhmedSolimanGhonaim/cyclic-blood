from django.db import models

class Donor(models.Model):
    id = models.AutoField(primary_key=True)
    name=models.CharField(max_length=100)
    email=models.EmailField(max_length=100, unique=True)
    city=models.CharField(max_length=100)
    # last_donation_date
    last_donation_date = models.DateField(null=True, blank=True)
    can_donate = models.BooleanField(default=True)
    
    def __str__(self):
        return self.name
    
