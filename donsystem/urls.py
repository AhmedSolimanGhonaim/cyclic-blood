
from django.contrib import admin
from django.urls import path , include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('users.urls')),
    path('api/donor/', include('donor.urls')),
    path('api/hospital/', include('hospital.urls')),
    path('api/bloodrequests/', include('bloodrequests.urls')),
    path('api/patient/', include('patient.urls')),
    path('api/donation/', include('donation.urls')),
    path('api/bloodbank/',include('bloodbank.urls')),
    path('api/stock/', include('bloodstock.urls'))
    # path('api/auth/', include('rest_framework.urls')),
]
