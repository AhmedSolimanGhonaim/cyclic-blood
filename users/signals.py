# # users/signals.py
# from django.db.models.signals import post_save
# from django.dispatch import receiver
# from django.conf import settings
# from donor.models import Donor
# from hospital.models import Hospital  # If exists

# User = settings.AUTH_USER_MODEL  # This equals CustomUser


# @receiver(post_save, sender=User)
# def create_profile(sender, instance, created, **kwargs):
#     if created:
#         if instance.role == 'donor':
#             Donor.objects.create(
#                 user=instance,
#                 name=instance.get_full_name(), 
#                 email=instance.email,
#                 city=instance.city,
#                 national_id='TEMP-ID',  
#                 phone='',
#             )
#         elif instance.role == 'hospital':
#             Hospital.objects.create(
#                 user=instance,
#                 name=instance.username,
#                 city=instance.city,
#                 phone='',
#                 address=''
#             )
