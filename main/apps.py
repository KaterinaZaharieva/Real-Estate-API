""" import  Django registry of installed applications that stores
 configuration and provides introspection """
from django.apps import AppConfig

class MainConfig(AppConfig):
    """ configurating AppConfig """
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'main'
