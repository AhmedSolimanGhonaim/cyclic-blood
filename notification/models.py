from django.db import models

# Create your models here.

class Notification(models.Model):
    id=models.AutoField(primary_key=True)
    message = models.TextField()
    status = models.BooleanField(default=False, help_text="True = Read, False = Unread")
    sent_at = models.DateTimeField(auto_now_add=True)
    via_email = models.BooleanField(default=False, help_text="True = Sent via Email, False = Not Sent")
    donation = models.ForeignKey(
        'donation.Donation', 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        related_name='notifications'
    )
    donor = models.ForeignKey(
        'donor.Donor', 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        related_name='notifications'
    )
    @property
    def is_read(self):
        """Check if the notification is read"""
        return self.status
    def __str__(self):
        return f"Notification {self.id} - {'Read' if self.status else 'Unread'}"