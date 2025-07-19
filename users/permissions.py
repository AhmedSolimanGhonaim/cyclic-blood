from rest_framework.permissions import BasePermission


class IsDonorUser(BasePermission):
    """
    Custom permission to only allow donors to access donor-specific endpoints.
    """
    def has_permission(self, request, view):
        return (
            request.user and 
            request.user.is_authenticated and 
            hasattr(request.user, 'donor_profile') and
            request.user.donor_profile is not None
        )


class IsHospitalUser(BasePermission):
    """
    Custom permission to only allow hospitals to access hospital-specific endpoints.
    """
    def has_permission(self, request, view):
        return (
            request.user and 
            request.user.is_authenticated and 
            hasattr(request.user, 'hospital_profile') and
            request.user.hospital_profile is not None
        )


class IsBankEmployeeUser(BasePermission):
    """
    Custom permission to only allow bank employees to access bank-specific endpoints.
    """
    def has_permission(self, request, view):
        return (
            request.user and 
            request.user.is_authenticated and 
            hasattr(request.user, 'bank_employee_profile') and
            request.user.bank_employee_profile is not None
        )


class IsOwnerOrReadOnly(BasePermission):
    """
    Custom permission to only allow owners of an object to edit it.
    """
    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed for any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in ['GET', 'HEAD', 'OPTIONS']:
            return True

        # Write permissions are only allowed to the owner of the object.
        return obj.user == request.user


class IsOwnerHospital(BasePermission):
    """
    Custom permission to only allow hospitals to access their own patients/requests.
    """
    def has_object_permission(self, request, view, obj):
        if not hasattr(request.user, 'hospital_profile'):
            return False
        
        # Check if the object belongs to the hospital
        if hasattr(obj, 'hospital'):
            return obj.hospital == request.user.hospital_profile
        
        return False


class IsOwnerDonor(BasePermission):
    """
    Custom permission to only allow donors to access their own donations.
    """
    def has_object_permission(self, request, view, obj):
        if not hasattr(request.user, 'donor_profile'):
            return False
        
        # Check if the object belongs to the donor
        if hasattr(obj, 'donor'):
            return obj.donor == request.user.donor_profile
        
        return False
