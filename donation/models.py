from django.db import models

from datetime import timedelta,date

class BloodType(models.TextChoices):
    A_POS = 'A+', 'A Positive'
    A_NEG = 'A-', 'A Negative'
    B_POS = 'B+', 'B Positive'
    B_NEG = 'B-', 'B Negative'
    AB_POS = 'AB+', 'AB Positive'
    AB_NEG = 'AB-', 'AB Negative'
    O_POS = 'O+', 'O Positive'
    O_NEG = 'O-', 'O Negative'



class DonationStatus(models.TextChoices):
    PENDING = 'pending', 'Pending'
    REJECTED_VIRUS = 'rejected_virus', 'Rejected (Virus Positive)'
    REJECTED_TIME = 'rejected_time', 'Rejected (Too Soon)'
    ACCEPTED = 'accepted', 'Accepted'


# the real model
class Donation(models.Model):
    id = models.AutoField(primary_key=True)

    donor = models.ForeignKey('donor.Donor', on_delete=models.SET_NULL, null=True, blank=True,related_name='donations')

    donation_date = models.DateField(
        verbose_name="Donation Date", auto_now_add=True
    )
    
    virus_test_result = models.BooleanField(
       default=False, 
        help_text="True = Negative (Safe), False = Positive (Unsafe)"
    )
    blood_type = models.CharField(
        max_length=3,
        choices=BloodType.choices
    )
    quantity_ml=models.IntegerField(
        default=450,)
    bank = models.ForeignKey(
        'bloodbank.BloodBank', on_delete=models.SET_NULL, null=True, blank=True , related_name='donations'
    )
    status = models.CharField(
        max_length=20,
        choices=DonationStatus.choices,
        default=DonationStatus.PENDING,
    )
    expiration_date = models.DateField(null=True, blank=True)
    rejection_reason = models.TextField(blank=True)
    

    from datetime import timedelta

    def save(self, *args, **kwargs):
        # Set expiration date (42 days from donation)
        if not self.expiration_date:
            self.expiration_date = self.donation_date + timedelta(days=42)
        super().save(*args, **kwargs)
        
        
    def evaluate_donation(self):
        """Evaluate donation based on business rules"""
        # Check virus test (True = negative = safe)
        if not self.virus_test_result:
            self.status = DonationStatus.REJECTED_VIRUS
            self.rejection_reason = "Virus test came back positive"
            return False
            # time check
        if not self.donor.can_donate:
            self.status = DonationStatus.REJECTED_TIME
            self.rejection_reason = f"Must wait {self.donor.days_until_next_donation} more days"
            return False
    
        self.status = DonationStatus.ACCEPTED
        self.rejection_reason = ""

        # Update donor's last donation date
        self.donor.last_donation_date = self.donation_date
        self.donor.total_donations += 1
        self.donor.save()
   
    @property
    def is_expired(self):
        return date.today() > self.expiration_date
    
    @property
    def days_until_expiry(self):
        return (self.expiration_date - date.today()).days

    def __str__(self):
        return f"Donation #{self.id} - {self.donor.name} - {self.status}"
