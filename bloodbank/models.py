from django.db import models

from django.contrib.gis.db import models as geomodels


class BankEmployee(models.Model):
    user = models.OneToOneField('users.CustomUser', on_delete=models.SET_NULL,
                                null=True, blank=True,  related_name='bank_employee_profile')
    blood_bank = models.ForeignKey(
        'bloodbank.BloodBank', on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"{self.user.username} at {self.blood_bank.name}"


class BloodBank(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=200)
    city = models.ForeignKey('city.City', null=True,blank=True,on_delete=models.SET_NULL)
    location = geomodels.PointField(geography=True,null=True,blank=True)
    address = models.TextField(blank=True)
    email = models.EmailField(blank=True)
    phone = models.CharField(max_length=20, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.name} - {self.city}"
