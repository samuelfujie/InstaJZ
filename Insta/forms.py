from django import forms
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from Insta.models import InstaUser

# forms defined here to handle user input

class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = InstaUser
        fields = ('username', 'email', 'profile_pic')