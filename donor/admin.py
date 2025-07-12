from django.contrib import admin

from .models import  Donor

@admin.register(Donor)
class DonorAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'city', 'last_donation_date', 'can_donate')
    search_fields = ('name', 'email', 'city')
    readonly_fields = ('registration_date', 'updated_at','can_donate')
    list_filter = ('can_donate', 'city')