from celery import shared_task
from django.utils import timezone
from .models import Stock , StockStatus
from matchersystem.services import batch_match_requests






@shared_task
def expire_old_stocks():
    today = timezone.now().date()
    expired = Stock.objects.filter(status= StockStatus.AVAILABLE,donation__expiration_date__lt=today)
    count = expired.update(status=StockStatus.EXPIRED)
    return f"Marked {count} as expired"


@shared_task
def run_batch_matching():
    return batch_match_requests()
