from bloodrequests.models import BloodRequests
from .models import Matcher
from bloodstock.models import Stock, StockStatus
from django.utils import timezone
from django.db import models
PRIORITY_ORDER = {
    'immediate': 1,
    'urgent': 2,
    'normal': 3
}


def match_blood_request(request):
    quantity_needed = request.quantity
    matched_quantity = 0

    available_stocks = Stock.objects.filter(
        status=StockStatus.AVAILABLE,
        blood_type=request.blood_type,
        city=request.city,
        donation__expiration_date__gt=timezone.now()
    ).order_by('created_at')

    for stock in available_stocks:
        if quantity_needed <= 0:
            break

        allocatable = min(stock.quantity, quantity_needed)

        Matcher.objects.create(
            request_id=request,
            stock_id=stock,
            quantity_allocated=allocatable
        )

        stock.mark_used(allocatable)

        matched_quantity += allocatable
        quantity_needed -= allocatable

    request.status = 'fulfilled' if matched_quantity >= request.quantity else 'pending'
    request.save()

def batch_match_requests():
    pending_requests = BloodRequests.objects.filter(status='pending')

    if pending_requests.count() < 10:
        return {"message": "At least 10 pending requests are required to process a batch."}

    # Prioritize requests
    sorted_requests = pending_requests.order_by(
        models.Case(
            *[models.When(priority=prio, then=val) for prio, val in PRIORITY_ORDER.items()]
        ),
        'requested_at'
    )

    matched = []
    for req in sorted_requests:
        match_blood_request(req)
        matched.append(req.id)

    return {"matched_requests": matched}
