from django.db import models

# Create your models here.
class Matcher(models.Model):
    id = models.AutoField(primary_key=True)
    stock_id = models.ForeignKey('bloodstock.Stock', on_delete=models.CASCADE, related_name='matchers')
    request_id = models.ForeignKey('bloodrequests.BloodRequests', on_delete=models.SET_NULL, related_name='matchers')
    quantity_allocated = models.PositiveIntegerField(default=0,null=False,blank=False)
    
    def __str__(self):
        return f"Matcher {self.id}"