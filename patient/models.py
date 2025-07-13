from django.db import models

from hospital.models import Hospital
PRIORITY_CHOICES = [
    ('immediate', 'Immediate'),
    ('normal', 'Normal'),
    ('urgent', 'Urgent')
]
class Patient(models.Model):
    name = models.CharField(max_length=100)
    age = models.PositiveIntegerField()
    blood_type = models.CharField(max_length=3 , choices = [
        ('A+', 'A Positive'),
        ('A-', 'A Negative'),
        ('B+', 'B Positive'),
        ('B-', 'B Negative'),
        ('AB+', 'AB Positive'),
        ('AB-', 'AB Negative'),
        ('O+', 'O Positive'),
        ('O-', 'O Negative')
    ])
    hospital = models.ForeignKey(Hospital,on_delete = models.SET_NULL, null=True, blank=True, related_name='patients')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=20 , choices=PRIORITY_CHOICES, default='normal')
    
    def __str__(self):
        return f"{self.name} - {self.blood_type} - {self.status} - {self.age} years"

    