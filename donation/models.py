from django.db import models

from datetime import timedelta, date

from django.core.mail import send_mail

from django.conf import settings

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


class Donation(models.Model):
    id = models.AutoField(primary_key=True)

    donor = models.ForeignKey('donor.Donor', on_delete=models.SET_NULL,
                              null=True, blank=True, related_name='donations')

    donation_date = models.DateField(
        verbose_name="Donation Date", auto_now_add=True
    )

    virus_test_result = models.BooleanField(
        null=True,blank=True
    )

    blood_type = models.CharField(
        max_length=3,
        choices=BloodType.choices
    )
    quantity_ml = models.IntegerField(
        default=1)
    bank = models.ForeignKey(
        'bloodbank.BloodBank', on_delete=models.SET_NULL, null=True, blank=True, related_name='donations'
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
        
        if not self.donation_date:
            self.donation_date = date.today()
        if not self.expiration_date:
            self.expiration_date = self.donation_date + timedelta(days=42)
        super().save(*args, **kwargs)

    def evaluate_donation(self):
        """Evaluate donation based on business rules"""
        self.expiration_date = date.today() + timedelta(days=42)
        
        if self.virus_test_result is None:
            self.status = DonationStatus.PENDING
            self.rejection_reason = "Awaiting virus test result"
            return False
            # time check
        # Case 1: Virus test failed
        if self.virus_test_result is False:
            self.status = DonationStatus.REJECTED_VIRUS
            self.rejection_reason = "Virus test came back positive"
            self.send_rejection_email()
            return False

        # Case 2: Not eligible by time
        if not self.donor.can_donate:
            self.status = DonationStatus.REJECTED_TIME
            
            self.rejection_reason = f"Must wait {self.donor.days_until_next_donation} more days"
            self.send_rejection_email()
            return False
            # Case 3: Accepted
        self.status = DonationStatus.ACCEPTED
        self.rejection_reason = ""
        self.donor.last_donation_date = self.donation_date or date.today()
        self.donor.total_donations += 1
        self.donor.save()
        return True

    @property
    def is_expired(self):
        return date.today() > self.expiration_date

    @property
    def days_until_expiry(self):
        return (self.expiration_date - date.today()).days

    def send_rejection_email(self):
        if self.donor and self.donor.user and self.donor.user.email:

            send_mail(
                subject="Donation Rejected",
                message=f"Dear {self.donor.name}, your donation was rejected due to: {self.rejection_reason}",
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[self.donor.user.email],
                fail_silently=True
            )
    def __str__(self):
        return f"Donation #{self.id} - {self.donor.name} - {self.status}"
