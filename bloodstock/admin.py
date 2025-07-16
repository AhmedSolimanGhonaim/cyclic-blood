from django.contrib import admin
from .models import Stock


@admin.register(Stock)
class DonationAdmin(admin.ModelAdmin):
    list_filter = ('status','blood_type')
