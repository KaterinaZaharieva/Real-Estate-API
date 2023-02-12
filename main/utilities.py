""" importing the database module for Notifications"""
from .models import Notification

def create_notification(request, to_user, notification_type, extra_id=0):
    """creating notification"""
    notification = Notification.objects.create(to_user=to_user,
                                                otification_type=notification_type, created_by=request.user, extra_id=extra_id)
