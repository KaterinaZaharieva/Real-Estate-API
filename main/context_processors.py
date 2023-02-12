#""" importing the database module for Notifications"""
#from .models import Notification

def notifications(request):
    """ making notifications appear as number if not readed"""
    if request.user.is_authenticated:
        return {'notifications': request.user.notifications.filter(is_read=False)}
    return {'notifications': []}
