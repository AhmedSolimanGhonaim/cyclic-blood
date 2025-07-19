from django.utils import timezone
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.conf import settings
from datetime import timedelta, date
from .models import Notification, SystemAlert, NotificationType, NotificationPriority
from bloodstock.models import Stock
from donation.models import Donation
from bloodrequests.models import BloodRequest

User = get_user_model()

class NotificationService:
    """Comprehensive notification service with automation features"""
    
    @staticmethod
    def create_notification(user, title, message, notification_type=NotificationType.SYSTEM_ALERT, 
                          priority=NotificationPriority.MEDIUM, send_email=False, **kwargs):
        """Create a new notification"""
        notification = Notification.objects.create(
            user=user,
            title=title,
            message=message,
            notification_type=notification_type,
            priority=priority,
            donation=kwargs.get('donation'),
            stock=kwargs.get('stock'),
            blood_request=kwargs.get('blood_request')
        )
        
        if send_email:
            NotificationService.send_email_notification(notification)
        
        return notification
    
    @staticmethod
    def send_email_notification(notification):
        """Send email notification"""
        try:
            send_mail(
                subject=f"[Blood Donation System] {notification.title}",
                message=notification.message,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[notification.user.email],
                fail_silently=False,
            )
            notification.is_sent_email = True
            notification.save(update_fields=['is_sent_email'])
        except Exception as e:
            print(f"Failed to send email notification: {e}")
    
    @staticmethod
    def notify_donation_accepted(donation):
        """Notify donor when donation is accepted"""
        if donation.donor and donation.donor.user:
            title = "Donation Accepted - Thank You!"
            message = f"""
            Great news! Your blood donation from {donation.donation_date} has been accepted 
            and added to our blood stock. Your contribution will help save lives!
            
            Donation Details:
            - Blood Type: {donation.blood_type}
            - Quantity: {donation.quantity_ml}ml
            - Bank: {donation.bank.name if donation.bank else 'N/A'}
            
            Thank you for your generosity!
            """
            
            NotificationService.create_notification(
                user=donation.donor.user,
                title=title,
                message=message,
                notification_type=NotificationType.DONATION_ACCEPTED,
                priority=NotificationPriority.MEDIUM,
                send_email=True,
                donation=donation
            )
    
    @staticmethod
    def notify_donation_rejected(donation, reason):
        """Notify donor when donation is rejected"""
        if donation.donor and donation.donor.user:
            title = "Donation Update - Important Information"
            message = f"""
            We regret to inform you that your blood donation from {donation.donation_date} 
            could not be accepted for the following reason: {reason}
            
            Donation Details:
            - Blood Type: {donation.blood_type}
            - Quantity: {donation.quantity_ml}ml
            - Bank: {donation.bank.name if donation.bank else 'N/A'}
            
            Please don't be discouraged! You can donate again after the recommended waiting period.
            Thank you for your willingness to help save lives.
            """
            
            NotificationService.create_notification(
                user=donation.donor.user,
                title=title,
                message=message,
                notification_type=NotificationType.DONATION_REJECTED,
                priority=NotificationPriority.HIGH,
                send_email=True,
                donation=donation
            )
    
    @staticmethod
    def check_and_notify_expiring_stock():
        """Check for expiring stock and send notifications"""
        # Check for stock expiring in the next 7 days
        warning_date = timezone.now().date() + timedelta(days=7)
        expiring_stock = Stock.objects.filter(
            expiration_date__lte=warning_date,
            expiration_date__gt=timezone.now().date(),
            quantity__gt=0
        )
        
        for stock in expiring_stock:
            # Notify blood bank employees
            bank_employees = User.objects.filter(
                role='bank_employee',
                bank_employee_profile__blood_bank=stock.blood_bank
            )
            
            days_until_expiry = (stock.expiration_date - timezone.now().date()).days
            
            for employee in bank_employees:
                title = f"Stock Expiring Soon - {stock.blood_type}"
                message = f"""
                URGENT: Blood stock is expiring soon!
                
                Stock Details:
                - Blood Type: {stock.blood_type}
                - Quantity: {stock.quantity}ml
                - Expiry Date: {stock.expiration_date}
                - Days Until Expiry: {days_until_expiry}
                - Blood Bank: {stock.blood_bank.name}
                
                Please prioritize this stock for distribution or take necessary action.
                """
                
                priority = NotificationPriority.CRITICAL if days_until_expiry <= 3 else NotificationPriority.HIGH
                
                NotificationService.create_notification(
                    user=employee,
                    title=title,
                    message=message,
                    notification_type=NotificationType.STOCK_EXPIRY,
                    priority=priority,
                    send_email=True,
                    stock=stock
                )
    
    @staticmethod
    def check_and_notify_expired_stock():
        """Check for expired stock and send notifications"""
        expired_stock = Stock.objects.filter(
            expiration_date__lt=timezone.now().date(),
            quantity__gt=0
        )
        
        for stock in expired_stock:
            # Mark stock as expired and notify
            bank_employees = User.objects.filter(
                role='bank_employee',
                bank_employee_profile__blood_bank=stock.blood_bank
            )
            
            for employee in bank_employees:
                title = f"Stock Expired - Immediate Action Required"
                message = f"""
                CRITICAL: Blood stock has expired and must be removed!
                
                Stock Details:
                - Blood Type: {stock.blood_type}
                - Quantity: {stock.quantity}ml
                - Expiry Date: {stock.expiration_date}
                - Blood Bank: {stock.blood_bank.name}
                
                Please remove this stock immediately and update inventory.
                """
                
                NotificationService.create_notification(
                    user=employee,
                    title=title,
                    message=message,
                    notification_type=NotificationType.STOCK_EXPIRY,
                    priority=NotificationPriority.CRITICAL,
                    send_email=True,
                    stock=stock
                )
            
            # Set quantity to 0 to mark as expired
            stock.quantity = 0
            stock.save()
    
    @staticmethod
    def create_system_alert(blood_bank, alert_type, title, description, severity=NotificationPriority.HIGH, affected_stock_ids=None):
        """Create system alert for power outages, storage issues, etc."""
        alert = SystemAlert.objects.create(
            blood_bank=blood_bank,
            alert_type=alert_type,
            title=title,
            description=description,
            severity=severity
        )
        
        # Add affected stock if provided
        if affected_stock_ids:
            affected_stock = Stock.objects.filter(id__in=affected_stock_ids)
            alert.affected_stock.set(affected_stock)
        
        # Notify all bank employees
        bank_employees = User.objects.filter(
            role='bank_employee',
            bank_employee_profile__blood_bank=blood_bank
        )
        
        for employee in bank_employees:
            NotificationService.create_notification(
                user=employee,
                title=title,
                message=description,
                notification_type=NotificationType.SYSTEM_ALERT,
                priority=severity,
                send_email=True
            )
        
        return alert
    
    @staticmethod
    def handle_power_outage(blood_bank, duration_hours, affected_stock_ids=None):
        """Handle power outage scenario"""
        title = f"CRITICAL: Power Outage at {blood_bank.name}"
        description = f"""
        EMERGENCY: Power outage detected at {blood_bank.name}
        
        Duration: {duration_hours} hours
        Impact: Blood storage temperature may be compromised
        
        Immediate Actions Required:
        1. Check backup power systems
        2. Monitor storage temperatures
        3. Assess affected blood stock
        4. Consider emergency transfer if needed
        
        This is a critical alert requiring immediate attention!
        """
        
        alert = NotificationService.create_system_alert(
            blood_bank=blood_bank,
            alert_type='power_outage',
            title=title,
            description=description,
            severity=NotificationPriority.CRITICAL,
            affected_stock_ids=affected_stock_ids
        )
        
        # Mark affected stock as potentially spoiled
        if affected_stock_ids:
            affected_stock = Stock.objects.filter(id__in=affected_stock_ids)
            for stock in affected_stock:
                NotificationService.notify_stock_spoiled(stock, "Power outage - temperature compromise")
        
        return alert
    
    @staticmethod
    def handle_storage_failure(blood_bank, failure_type, affected_stock_ids=None):
        """Handle storage equipment failure"""
        title = f"Storage Equipment Failure at {blood_bank.name}"
        description = f"""
        ALERT: Storage equipment failure detected
        
        Failure Type: {failure_type}
        Blood Bank: {blood_bank.name}
        
        Actions Required:
        1. Assess equipment damage
        2. Check affected blood stock
        3. Arrange emergency storage if needed
        4. Contact maintenance team
        
        Monitor situation closely and take preventive measures.
        """
        
        return NotificationService.create_system_alert(
            blood_bank=blood_bank,
            alert_type='storage_failure',
            title=title,
            description=description,
            severity=NotificationPriority.HIGH,
            affected_stock_ids=affected_stock_ids
        )
    
    @staticmethod
    def notify_stock_spoiled(stock, reason):
        """Notify about spoiled stock due to storage issues"""
        bank_employees = User.objects.filter(
            role='bank_employee',
            bank_employee_profile__blood_bank=stock.blood_bank
        )
        
        for employee in bank_employees:
            title = f"Stock Spoiled - {stock.blood_type}"
            message = f"""
            ALERT: Blood stock has been compromised and marked as spoiled
            
            Stock Details:
            - Blood Type: {stock.blood_type}
            - Quantity: {stock.quantity}ml
            - Reason: {reason}
            - Blood Bank: {stock.blood_bank.name}
            
            Please remove this stock immediately and update inventory records.
            """
            
            NotificationService.create_notification(
                user=employee,
                title=title,
                message=message,
                notification_type=NotificationType.STOCK_SPOILED,
                priority=NotificationPriority.HIGH,
                send_email=True,
                stock=stock
            )
        
        # Mark stock as spoiled (set quantity to 0)
        stock.quantity = 0
        stock.save()
    
    @staticmethod
    def notify_blood_request_created(blood_request):
        """Notify about new blood request"""
        # Notify blood bank employees in the same city
        bank_employees = User.objects.filter(
            role='bank_employee',
            bank_employee_profile__blood_bank__city=blood_request.hospital.user.city
        )
        
        for employee in bank_employees:
            title = f"New Blood Request - {blood_request.blood_type}"
            message = f"""
            New blood request received:
            
            Request Details:
            - Blood Type: {blood_request.blood_type}
            - Quantity: {blood_request.quantity}ml
            - Priority: {blood_request.priority}
            - Hospital: {blood_request.hospital.name}
            - Patient: {blood_request.patient.name}
            
            Please check stock availability and process the request.
            """
            
            priority = NotificationPriority.HIGH if blood_request.priority == 'high' else NotificationPriority.MEDIUM
            
            NotificationService.create_notification(
                user=employee,
                title=title,
                message=message,
                notification_type=NotificationType.BLOOD_REQUEST,
                priority=priority,
                send_email=True,
                blood_request=blood_request
            )
    
    @staticmethod
    def get_user_notifications(user, unread_only=False):
        """Get notifications for a user"""
        queryset = Notification.objects.filter(user=user)
        if unread_only:
            queryset = queryset.filter(is_read=False)
        return queryset.order_by('-created_at')
    
    @staticmethod
    def mark_notifications_as_read(user, notification_ids=None):
        """Mark notifications as read"""
        queryset = Notification.objects.filter(user=user, is_read=False)
        if notification_ids:
            queryset = queryset.filter(id__in=notification_ids)
        
        for notification in queryset:
            notification.mark_as_read()
    
    @staticmethod
    def get_unread_count(user):
        """Get count of unread notifications for a user"""
        return Notification.objects.filter(user=user, is_read=False).count()
