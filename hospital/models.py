from django.db import models

from django.contrib.auth import get_user_model
from django.contrib.gis.db import models as geomodels

User = get_user_model()

class Hospital(models.Model):
    user = models.OneToOneField(User, related_name='hospital_profile', on_delete=models.SET_NULL, null=True, blank=True)
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=200)
    phone = models.CharField(max_length=20, blank=True,null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    # city = models.CharField(user.city.name, max_length=50)
    # location = geomodels.PointField(geography=True,blank=True,null=True , default=user.city.location)

    def __str__(self):
        return f"{self.name} - {self.city}"
   
    def get_nearest_blood_bank(self):
        """
        Placeholder for a method to get the nearest blood bank.
        This would typically involve some logic to find the closest blood bank
        based on the hospital's location.
        """
        return "Nearest Blood Bank Logic to be implemented"
  
  