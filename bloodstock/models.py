from django.db import models

# Create your models here.
from donation.models import Donation


class StockStatus(models.TextChoices):  # Renamed for clarity
    AVAILABLE = 'available', 'Available'
    EXPIRED = 'expired', 'Expired'
    USED = 'used', 'Used'


class BloodType(models.TextChoices):
    A_POS = 'A+', 'A Positive'
    A_NEG = 'A-', 'A Negative'
    B_POS = 'B+', 'B Positive'
    B_NEG = 'B-', 'B Negative'
    AB_POS = 'AB+', 'AB Positive'
    AB_NEG = 'AB-', 'AB Negative'
    O_POS = 'O+', 'O Positive'
    O_NEG = 'O-', 'O Negative'


class Stock(models.Model):
    id = models.AutoField(primary_key=True)
    donation = models.OneToOneField(
        Donation, on_delete=models.SET_NULL, null=True, blank=True, related_name='stock')
    blood_type = models.CharField(
        max_length=3,
        choices=BloodType.choices
    )
    status = models.CharField(
        max_length=20,
        choices=StockStatus.choices,
        default=StockStatus.AVAILABLE
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
