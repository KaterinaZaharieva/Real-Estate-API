""" import moduls from django to create forms, users and posts"""
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Post, ReviewRating

class RegisterForm(UserCreationForm):
    """ form for creating users"""
    email = forms.EmailField(required=True)
    group = forms.ChoiceField(choices=[("buyer", "Buyer"), ("agent", "Agent")])
    class Meta:
        """ Meta """
        model = User
        fields = ["username","email","password1","password2","group"]

class PostForm(forms.ModelForm):
    """ form for creating posts"""
    class Meta:
        """ Meta """
        model = Post
        fields = ["title", "description","post_image"]

class ReviewForm (forms.ModelForm):
    class Meta:
        model = ReviewRating
        fields = ['rating']