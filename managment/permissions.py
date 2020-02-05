from rest_framework.permissions import BasePermission


class IsEventCreator(BasePermission):
    message = "Not the creator for the event"

    def has_object_permission(self, request, view, obj):
        return request.user == obj.created_by
