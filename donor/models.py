from django.db import models
from datetime import date
from django.contrib.auth import get_user_model

User = get_user_model()

class Donor(models.Model):
    """Model representing a donor."""
    user = models.OneToOneField(User,related_name='donor_profile', on_delete=models.SET_NULL, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    id = models.AutoField(primary_key=True)
    national_id = models.CharField(unique=True, max_length=20)
    name=models.CharField(max_length=100)
    # email=models.EmailField(max_length=100, unique=True)
    # city=models.CharField(max_length=100)
    last_donation_date = models.DateField(null=True, blank=True)
    can_donate = models.BooleanField(default=True)
    registration_date = models.DateField(auto_now_add=True)
    phone = models.CharField(max_length=20, blank=True)
    total_donations = models.IntegerField(default=0)
    blood_type = models.CharField(max_length=3, blank=True, null=True, help_text="Blood type is set after first donation and cannot be changed")
    updated_at = models.DateTimeField(auto_now=True)
    
    
    @property
    def days_until_next_donation(self):
        """Return days left until donor can donate again."""
        if self.last_donation_date:
            days_passed = (date.today() - self.last_donation_date).days
            return max(0, 90 - days_passed)
        return 0

    def save(self, *args, **kwargs):
        """ can donate manipulation  """
        if self.last_donation_date:
            days_passed = (date.today()-self.last_donation_date).days
            self.can_donate = days_passed >=90
        else:
            self.can_donate = True
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        self.is_active = False
        self.save()
    def __str__(self):
        return f"{self.name} ({self.national_id})"


    def __str__(self):
        return self.name
    