from bloodrequests.models import BloodRequests
from .models import Matcher
from bloodstock.models import Stock, StockStatus
from django.utils import timezone
from django.db import models
from django.contrib.gis.db.models.functions import Distance

PRIORITY_ORDER = {
    'immediate': 1,
    'urgent': 2,
    'normal': 3
}


def match_blood_request(request):
    quantity_needed = request.quantity
    matched_quantity = 0
    requested_location = request.hospital.user.location if request.hospital and request.hospital.user else None
    if not requested_location:
        return 
    available_stocks = Stock.objects.filter(
        status=StockStatus.AVAILABLE,
        blood_type=request.blood_type,
        donation__expiration_date__gt=timezone.now()
    ).annotate(distance=Distance('bank__location',requested_location)).order_by('distance','created_at')

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
    """Process batch matching for 10+ pending requests based on priority and distance"""
    pending_requests = BloodRequests.objects.filter(status='pending')

    if pending_requests.count() < 10:
        return {
            "success": False,
            "message": f"At least 10 pending requests are required to process a batch. Currently have {pending_requests.count()} pending requests."
        }

    from bloodbank.models import BloodBank
    blood_banks = BloodBank.objects.filter(location__isnull=False)
    
    if not blood_banks.exists():
        return {
            "success": False,
            "message": "No blood banks with location data available for distance calculation."
        }

    requests_with_distance = []
    for req in pending_requests:
        if req.hospital and req.hospital.user and req.hospital.user.location:
            nearest_banks = blood_banks.annotate(
                distance=Distance('location', req.hospital.user.location)
            ).order_by('distance')[:1]
            
            if nearest_banks:
                distance_to_nearest = nearest_banks[0].distance.km if nearest_banks[0].distance else float('inf')
            else:
                distance_to_nearest = float('inf')
        else:
            distance_to_nearest = float('inf')
        
        requests_with_distance.append({
            'request': req,
            'priority_order': PRIORITY_ORDER.get(req.priority, 999),
            'distance': distance_to_nearest,
            'requested_at': req.requested_at
        })
    
    sorted_requests = sorted(requests_with_distance, key=lambda x: (
        x['priority_order'],  
        x['distance'],        
        x['requested_at']     
    ))

    matched_results = []
    failed_matches = []
    total_matched = 0
    
    for req_data in sorted_requests:
        req = req_data['request']
        try:
            original_status = req.status
            match_blood_request(req)
            req.refresh_from_db()
            
            result = {
                'request_id': req.id,
                'hospital': req.hospital.name if req.hospital else 'Unknown',
                'blood_type': req.blood_type,
                'quantity': req.quantity,
                'priority': req.priority,
                'distance_km': round(req_data['distance'], 2) if req_data['distance'] != float('inf') else 'Unknown',
                'status': req.status,
                'matched': req.status == 'fulfilled'
            }
            
            if req.status == 'fulfilled':
                matched_results.append(result)
                total_matched += 1
            else:
                failed_matches.append(result)
                
        except Exception as e:
            failed_matches.append({
                'request_id': req.id,
                'error': str(e),
                'status': 'error'
            })

    return {
        "success": True,
        "message": f"Batch processing completed. {total_matched} requests matched out of {len(sorted_requests)} processed.",
        "total_processed": len(sorted_requests),
        "total_matched": total_matched,
        "total_failed": len(failed_matches),
        "matched_requests": matched_results,
        "failed_requests": failed_matches,
        "processing_order": "Priority (immediate > urgent > normal) → Distance (nearest first) → Time (earliest first)"
    }
