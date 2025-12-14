from rest_framework import permissions

class IsOwnerOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
#we're using has_permissions because we want to block POST to anyone that's not a mentor.
#Allow anyone to get
        if request.method in permissions.SAFE_METHODS:
            return True
#only mentors can post
        return request.user.is_authenticated and request.user.is_mentor()
    
    def has_object_permission(self, request, view, obj):
        #allow anyone to read
        if request.method in permissions.SAFE_METHODS:
            return True
        #only the owner can update/delete
        return obj.owner == request.user

class IsMenteeOrReadOnly(permissions.BasePermission):

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user.is_authenticated and request.user.is_mentee()
    
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.mentee == request.user

class IsBookingOwnerOrReadOnly(permissions.BasePermission):

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user.is_authenticated and request.user.is_mentor()
    
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.fundraiser.owner == request.user
