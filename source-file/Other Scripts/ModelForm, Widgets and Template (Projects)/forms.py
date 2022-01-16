from django.forms import ModelForm
from .models import Project
from django import forms


class projectForm(ModelForm):
    class Meta:
        model = Project
        fields = ['title', 'featured_image', 'description', 'demo_link', 'source_link', 'tags']
        widgets = {
            'title': forms.TextInput(
                attrs={
                    'class': 'input input--text',
                    'placeholder': 'Enter text',
                    'type': 'text',
                    'name': 'text'
                    }
            ),
            'featured_image': forms.FileInput(
                attrs={
                    'class': 'input input--text',
                    'type': 'file',
                    }
            ),
            'description': forms.Textarea(
                attrs={
                    'class': 'input input--text',
                    'name': 'message',
                    'id': 'formInput#textarea',
                    'placeholder': 'Enter description',
                    }
            ),
            'demo_link': forms.URLInput(
                attrs={
                    'class': 'input input--text',
                    'type': 'text',
                    'placeholder': 'Enter demo link',
                    }
            ),
            'source_link': forms.URLInput(
                attrs={
                    'class': 'input input--text',
                    'type': 'text',
                    'placeholder': 'Enter source link',
                    }
            ),
            'tags': forms.CheckboxSelectMultiple(
                attrs={
                    'class': 'input input--checkbox',
                    'style': 'margin-right: 1rem;',
                    }
            )
        }
