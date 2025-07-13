from django.contrib import admin

from .models import  Donor

@admin.register(Donor)
class DonorAdmin(admin.ModelAdmin):
    list_display = ('name', 'national_id', 'last_donation_date', 'can_donate')
    list_filter = ('can_donate',)
    search_fields = ('name', 'national_id')
    