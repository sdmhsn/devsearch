from django.db.models import fields
from django.db.models.fields import Field
from django.forms import ModelForm, widgets
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from .models import Profile, Skill, Message


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['first_name', 'email', 'username', 'password1', 'password2']
        labels = {
            'first_name': 'Name'
        }
        
    def __init__(self, *args, **kwargs):
        super(CustomUserCreationForm, self).__init__(*args, **kwargs)
        # self.fields['first_name'].widget = forms.PasswordInput(attrs={'placeholder': "e.g. Dennis Ivanov"})
        # self.fields['email'].widget = forms.PasswordInput(attrs={'placeholder': "e.g. user@domain.com"})
        # self.fields['username'].widget = forms.PasswordInput(attrs={'placeholder': "e.g. username"})
        # self.fields['password1'].widget = forms.PasswordInput(attrs={'placeholder': "••••••••"})
        # self.fields['password2'].widget = forms.PasswordInput(attrs={'placeholder': "••••••••"})

        for name, field in self.fields.items():
            field.widget.attrs.update({'class': 'input input--text'})


class ProfileForm(ModelForm):
    class Meta:
        model = Profile
        # fields = '__all__'
        fields = [
            'name',
            'email',
            'username',
            'location',
            'bio',
            'short_intro',
            'profile_image',
            'social_github',
            'social_twitter',
            'social_linkedin',
            'social_youtube',
            'social_website'
        ]

    def __init__(self, *args, **kwargs):
        super(ProfileForm, self).__init__(*args, **kwargs)
    
        for name, field in self.fields.items():
            field.widget.attrs.update({'class': 'input input--text'})


class SkillForm(ModelForm):
    class Meta:
        model = Skill
        fields = '__all__'
        exclude = ['owner']  # id dan created secara default tidak tampil

    def __init__(self, *args, **kwargs):
        super(SkillForm, self).__init__(*args, **kwargs)

        for name, field in self.fields.items():
            field.widget.attrs.update({'class': 'input input--text'})


class MessageForm(ModelForm):
    class Meta:
        model = Message
        fields = ['name', 'email', 'subject', 'body']

    def __init__(self, *args, **kwargs):
        super(MessageForm, self).__init__(*args, **kwargs)

        for name, field in self.fields.items():
            field.widget.attrs.update({'class': 'input input--text'})
