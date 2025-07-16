from django.db import models

# Create your models here.
from donation.models import Donation
from django.core.exceptions import ValidationError
from django.db.models import Sum
class StockStatus(models.TextChoices):  
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

    quantity = models.PositiveIntegerField(default=0)
     
    bank= models.ForeignKey("bloodbank.BloodBank", null=True,blank=True, on_delete=models.SET_NULL)
    city = models.CharField(max_length=100, blank=True)


    @classmethod
    def count_available_blood_by_city(cls):
        stocks = cls.objects.filter(
            status=StockStatus.AVAILABLE,
            donation__expiration_date__gt=models.functions.Now()
        )
        total = stocks.values('city', 'blood_type').annotate(total=Sum('quantity'))

        result = {}
        for entry in total:
            city = entry['city']
            blood_type = entry['blood_type']
            quantity = entry['total']
            result.setdefault(city, {})[blood_type] = quantity
        return result

    def save(self, *args, **kwargs):
        if self.donation:
            if self.donation.status != 'accepted' or self.donation.virus_test_result is not True:
                raise ValidationError(
                    "Stock cannot be created for a donation that is not accepted and virus-free.")

            if not self.blood_type:
                self.blood_type = self.donation.blood_type
            if not self.quantity:
                self.quantity = self.donation.quantity_ml
            if self.donation and self.donation.bank:
                self.bank =self.donation.bank
                self.city =self.donation.bank.city
                
         
        super().save(*args, **kwargs)
            
    def __str__(self):
        return f"Stock {self.id} - {self.blood_type} - {self.status}"

