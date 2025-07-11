from django.db import models
from datetime import date
class Donor(models.Model):
    id = models.AutoField(primary_key=True)
    national_id = models.CharField(unique=True, max_length=20)
    name=models.CharField(max_length=100)
    email=models.EmailField(max_length=100, unique=True)
    city=models.CharField(max_length=100)
    # last_donation_date
    last_donation_date = models.DateField(null=True, blank=True)
    can_donate = models.BooleanField(default=True)
    registration_date = models.DateField(auto_now_add=True)
    phone = models.CharField(max_length=20, blank=True)
    total_donations = models.IntegerField(default=0)
    blood_type = models.CharField(
        max_length=4,
        blank=True,
        null=True
    )
    updated_at = models.DateTimeField(auto_now=True)
    @property
    def days_until_next_donation(self):
        """Calculate days until next eligible donation"""
        if self.last_donation_date:
            days_passed = (date.today() - self.last_donation_date).days
            return max(0, 90 - days_passed)
        return 0

    def __str__(self):
        return f"{self.name} ({self.national_id})"


    def __str__(self):
        return self.name
    
