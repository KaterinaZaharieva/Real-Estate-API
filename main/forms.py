""" import moduls from django to create forms, users, posts, reviews and inspections"""
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Post, ReviewRating, Inspection

class RegisterForm(UserCreationForm):
    """form for creating users"""
    email = forms.EmailField(required=True)
    group = forms.ChoiceField(choices=[("buyer", "Buyer"), ("agent", "Agent")])
    class Meta:
        """getting the model and making the fields in the form """
        model = User
        fields = ["username","email","password1","password2","group"]

class PostForm(forms.ModelForm):
    """form for creating posts"""
    class Meta:
        """getting the model and making the fields in the form """
        model = Post
        fields = ["title","city","price","contact_us", "description","post_image"]

class ReviewForm (forms.ModelForm):
    """form for creating review/rating"""
    class Meta:
        """getting the model and making the fields in the form"""
        model = ReviewRating
        fields = ['rating']

class InspectionForm(forms.ModelForm):
    """form for booking an inspection"""
    class Meta:
        """getting the model and making the fields in the form"""
        model = Inspection
        fields = ['date', 'contact_info']
