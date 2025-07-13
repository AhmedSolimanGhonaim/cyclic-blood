from django.db import models

# Create your models here.
class Hospital(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=200)
    # city = models.CharField(max_length=100)
    address = models.TextField(blank=True,null=True)
    # email = models.EmailField(blank=True,null=True)
    phone = models.CharField(max_length=20, blank=True,null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.city}"
    