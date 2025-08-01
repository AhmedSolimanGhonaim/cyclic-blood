from django.db import models

class BloodRequests(models.Model):
    
    id = models.AutoField(primary_key=True)
    hospital= models.ForeignKey('hospital.Hospital',on_delete=models.SET_NULL, null=True, blank=True, related_name='blood_requests')
    status = models.CharField(max_length=20, choices=[
        ('pending', 'Pending'),
        ('fulfilled', 'Fulfilled'),
        ('cancelled', 'Cancelled')
    ], default='pending')
    priority = models.CharField(max_length=10, choices=[
        ('immediate', 'Immediate'),
        ('normal', 'Normal'),
        ('urgent', 'Urgent')
    ], default='normal')
    updated_at = models.DateTimeField(auto_now=True)
    patient = models.ForeignKey('patient.Patient', on_delete=models.SET_NULL, null=True, blank=True, related_name='blood_requests')

    quantity = models.PositiveIntegerField(null=False, blank=False, default=1)
    requested_at = models.DateTimeField(auto_now_add=True)
    
    blood_type = models.CharField(max_length=3, choices=[
        ('A+', 'A Positive'),
        ('A-', 'A Negative'),
        ('B+', 'B Positive'),
        ('B-', 'B Negative'),
        ('AB+', 'AB Positive'),
        ('AB-', 'AB Negative'),
        ('O+', 'O Positive'),
        ('O-', 'O Negative')
    ], blank=True, null=True)
    def __str__(self):
        return f"Request {self.id} - {self.blood_type} - {self.quantity} units"