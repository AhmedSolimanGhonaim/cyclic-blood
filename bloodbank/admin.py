from django.contrib import admin

# Register your models here.
from .models import BloodBank


from django.contrib import admin


@admin.register(BloodBank)
class BankAdmin(admin.ModelAdmin):
    list_display = ('id', 'city','email', 'phone','address')
    search_fields = ('city', )
    
    
    #      id = models.AutoField(primary_key=True)
    # name = models.CharField(max_length=200)
    # city = models.CharField(max_length=100)
    # address = models.TextField(blank=True)
    # email = models.EmailField(blank=True)
    # phone = models.CharField(max_length=20, blank=True)
    # created_at = models.DateTimeField(auto_now_add=True)