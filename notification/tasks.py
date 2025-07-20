from celery import shared_task
from django.utils import timezone
from datetime import timedelta
from .services import NotificationService
from bloodstock.models import Stock
from bloodbank.models import BloodBank
import random

@shared_task
def check_expiring_stock():
    """Automated task to check for expiring stock"""
    try:
        NotificationService.check_and_notify_expiring_stock()
        return "Successfully checked expiring stock"
    except Exception as e:
        return f"Error checking expiring stock: {str(e)}"

@shared_task
def check_expired_stock():
    """Automated task to check for expired stock"""
    try:
        NotificationService.check_and_notify_expired_stock()
        return "Successfully checked expired stock"
    except Exception as e:
        return f"Error checking expired stock: {str(e)}"

@shared_task
def simulate_power_outage():
    """Simulate random power outage for demonstration"""
    try:
        blood_banks = BloodBank.objects.all()
        if not blood_banks:
            return "No blood banks available"
        
        blood_bank = random.choice(blood_banks)
        
        affected_stock = Stock.objects.filter(
            blood_bank=blood_bank,
            quantity__gt=0
        )[:random.randint(1, 3)]
        
        affected_stock_ids = [stock.id for stock in affected_stock]
        
        duration = random.randint(2, 8)
        
        alert = NotificationService.handle_power_outage(
            blood_bank=blood_bank,
            duration_hours=duration,
            affected_stock_ids=affected_stock_ids
        )
        
        return f"Simulated power outage at {blood_bank.name} for {duration} hours"
    except Exception as e:
        return f"Error simulating power outage: {str(e)}"

@shared_task
def simulate_storage_failure():
    """Simulate storage equipment failure for demonstration"""
    try:
        blood_banks = BloodBank.objects.all()
        if not blood_banks:
            return "No blood banks available"
        
        blood_bank = random.choice(blood_banks)
        
        affected_stock = Stock.objects.filter(
            blood_bank=blood_bank,
            quantity__gt=0
        )[:random.randint(1, 2)]
        
        affected_stock_ids = [stock.id for stock in affected_stock]
        
        failure_types = [
            "Refrigeration unit malfunction",
            "Temperature sensor failure", 
            "Backup generator failure",
            "Cooling system breakdown"
        ]
        
        failure_type = random.choice(failure_types)
        
        alert = NotificationService.handle_storage_failure(
            blood_bank=blood_bank,
            failure_type=failure_type,
            affected_stock_ids=affected_stock_ids
        )
        
        return f"Simulated storage failure at {blood_bank.name}: {failure_type}"
    except Exception as e:
        return f"Error simulating storage failure: {str(e)}"

@shared_task
def cleanup_old_notifications():
    """Clean up old read notifications (older than 30 days)"""
    try:
        from .models import Notification
        cutoff_date = timezone.now() - timedelta(days=30)
        
        old_notifications = Notification.objects.filter(
            is_read=True,
            read_at__lt=cutoff_date
        )
        
        count = old_notifications.count()
        old_notifications.delete()
        
        return f"Cleaned up {count} old notifications"
    except Exception as e:
        return f"Error cleaning up notifications: {str(e)}"

@shared_task
def daily_stock_report():
    """Generate daily stock report and send notifications"""
    try:
        from bloodstock.models import Stock
        from django.contrib.auth import get_user_model
        
        User = get_user_model()
        
        blood_banks = BloodBank.objects.all()
        
        for blood_bank in blood_banks:
            stock_summary = Stock.objects.filter(
                blood_bank=blood_bank,
                quantity__gt=0
            ).values('blood_type').annotate(
                total_quantity=models.Sum('quantity')
            )
            
            report_lines = [f"Daily Stock Report for {blood_bank.name}"]
            report_lines.append("=" * 50)
            
            total_units = 0
            for item in stock_summary:
                quantity = item['total_quantity'] or 0
                total_units += quantity
                report_lines.append(f"{item['blood_type']}: {quantity}ml")
            
            report_lines.append(f"\nTotal Stock: {total_units}ml")
            
            low_stock_types = []
            for item in stock_summary:
                if (item['total_quantity'] or 0) < 1000:  
                    low_stock_types.append(item['blood_type'])
            
            if low_stock_types:
                report_lines.append(f"\n  LOW STOCK WARNING:")
                report_lines.append(f"Blood types with low stock: {', '.join(low_stock_types)}")
            
            report_message = "\n".join(report_lines)
            
            bank_employees = User.objects.filter(
                role='bank_employee',
                bank_employee_profile__blood_bank=blood_bank
            )
            
            for employee in bank_employees:
                NotificationService.create_notification(
                    user=employee,
                    title=f"Daily Stock Report - {blood_bank.name}",
                    message=report_message,
                    notification_type='system_alert',
                    priority='low' if not low_stock_types else 'medium',
                    send_email=True
                )
        
        return f"Generated daily stock reports for {blood_banks.count()} blood banks"
    except Exception as e:
        return f"Error generating daily stock report: {str(e)}"
