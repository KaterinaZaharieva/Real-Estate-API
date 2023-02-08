"""import Django automatic admin interface
and  models to use Post"""
from django.contrib import admin
from . import models

class AuthorAdmin(admin.ModelAdmin):
    """ customizing the Post object in the admin site """
    list_display = ('title', 'author')

admin.site.register(models.Post, AuthorAdmin)
admin.site.register(models.ReviewRating)