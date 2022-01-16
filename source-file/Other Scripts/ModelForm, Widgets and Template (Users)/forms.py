from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['first_name', 'email', 'username', 'password1', 'password2']
        labels = {
            'first_name': 'Name'
        }
        # widgets = {
            # 'first_name': forms.TextInput(
                # attrs={
                    # 'placeholder': 'e.g. Dennis Ivanov',
                # }
            # ),
            # 'email': forms.TextInput(
                # attrs={
                    # 'placeholder': 'e.g. user@domain.com',
                # }
            # ),
            # 'username': forms.TextInput(
                # attrs={
                    # 'placeholder': 'e.g. username',
                # }
            # )
            # except password
        # }

    def __init__(self, *args, **kwargs):
        super(CustomUserCreationForm, self).__init__(*args, **kwargs)
        self.fields['first_name'].widget = forms.PasswordInput(attrs={'placeholder': "e.g. Dennis Ivanov"})
        self.fields['email'].widget = forms.PasswordInput(attrs={'placeholder': "e.g. user@domain.com"})
        self.fields['username'].widget = forms.PasswordInput(attrs={'placeholder': "e.g. username"})
        self.fields['password1'].widget = forms.PasswordInput(attrs={'placeholder': "••••••••"})
        self.fields['password2'].widget = forms.PasswordInput(attrs={'placeholder': "••••••••"})

        for name, field in self.fields.items():
            field.widget.attrs.update({'class': 'input input--text'})
