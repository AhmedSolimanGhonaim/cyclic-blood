from django.db import models

from django.contrib.auth import get_user_model

User = get_user_model()



class Hospital(models.Model):
    user = models.OneToOneField(User, related_name='hospital_profile', on_delete=models.SET_NULL, null=True, blank=True)
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=200)
    # city = models.CharField(max_length=100)
    address = models.TextField(blank=True,null=True)
    # email = models.EmailField(blank=True,null=True)
    phone = models.CharField(max_length=20, blank=True,null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.city}"
    def get_nearest_blood_bank(self):
        """
        Placeholder for a method to get the nearest blood bank.
        This would typically involve some logic to find the closest blood bank
        based on the hospital's location.
        """
        return "Nearest Blood Bank Logic to be implemented"
  
  
    # # def request_blood(self,blood_type, quantity):
    # #     location = self.user.city 
        
        
    #     """
    #     Placeholder for a method to request blood.
    #     This would typically involve some logic to handle the blood request.
    #     """
    #     return f"Requesting {quantity} units of {blood_type} blood"
    