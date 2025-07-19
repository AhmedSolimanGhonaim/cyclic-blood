from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone

User = get_user_model()

class NotificationType(models.TextChoices):
    DONATION_ACCEPTED = 'donation_accepted', 'Donation Accepted'
    DONATION_REJECTED = 'donation_rejected', 'Donation Rejected'
    STOCK_EXPIRY = 'stock_expiry', 'Stock Expiry'
    STOCK_SPOILED = 'stock_spoiled', 'Stock Spoiled'
    POWER_OUTAGE = 'power_outage', 'Power Outage Alert'
    STORAGE_ISSUE = 'storage_issue', 'Storage Issue'
    BLOOD_REQUEST = 'blood_request', 'Blood Request'
    SYSTEM_ALERT = 'system_alert', 'System Alert'

class NotificationPriority(models.TextChoices):
    LOW = 'low', 'Low'
    MEDIUM = 'medium', 'Medium'
    HIGH = 'high', 'High'
    CRITICAL = 'critical', 'Critical'

class Notification(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=200,default='unknown')
    message = models.TextField(default='')
    notification_type = models.CharField(
        max_length=20,
        choices=NotificationType.choices,
        default=NotificationType.SYSTEM_ALERT
    )
    priority = models.CharField(
        max_length=10,
        choices=NotificationPriority.choices,
        default=NotificationPriority.MEDIUM
    )
    is_read = models.BooleanField(default=False)
    is_sent_email = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True,null=True, blank=True)
    read_at = models.DateTimeField(null=True, blank=True)
    
    # Recipients
    user = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='notifications'
    )
    
    # Related objects
    donation = models.ForeignKey(
        'donation.Donation',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='notifications'
    )
    stock = models.ForeignKey(
        'bloodstock.Stock',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='notifications'
    )
    blood_request = models.ForeignKey(
        'bloodrequests.BloodRequests',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='notifications'
    )
    
    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['user', 'is_read']),
            models.Index(fields=['notification_type']),
            models.Index(fields=['priority']),
        ]
    
    def mark_as_read(self):
        """Mark notification as read"""
        if not self.is_read:
            self.is_read = True
            self.read_at = timezone.now()
            self.save(update_fields=['is_read', 'read_at'])
    
    def __str__(self):
        return f"{self.title} - {self.user.username} ({'Read' if self.is_read else 'Unread'})"

class SystemAlert(models.Model):
    """Model for system-wide alerts like power outages, storage issues"""
    id = models.AutoField(primary_key=True)
    alert_type = models.CharField(
        max_length=20,
        choices=[
            ('power_outage', 'Power Outage'),
            ('temperature_alert', 'Temperature Alert'),
            ('storage_failure', 'Storage Failure'),
            ('equipment_failure', 'Equipment Failure'),
        ]
    )
    title = models.CharField(max_length=200)
    description = models.TextField()
    blood_bank = models.ForeignKey(
        'bloodbank.BloodBank',
        on_delete=models.CASCADE,
        related_name='system_alerts'
    )
    severity = models.CharField(
        max_length=10,
        choices=NotificationPriority.choices,
        default=NotificationPriority.HIGH
    )
    is_resolved = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    resolved_at = models.DateTimeField(null=True, blank=True)
    
    # Affected stock
    affected_stock = models.ManyToManyField(
        'bloodstock.Stock',
        blank=True,
        related_name='system_alerts'
    )
    
    class Meta:
        ordering = ['-created_at']
    
    def resolve_alert(self):
        """Mark alert as resolved"""
        self.is_resolved = True
        self.resolved_at = timezone.now()
        self.save(update_fields=['is_resolved', 'resolved_at'])
    
    def __str__(self):
        return f"{self.title} - {self.blood_bank.name} ({'Resolved' if self.is_resolved else 'Active'})"