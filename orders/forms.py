from django import forms
from .models import Order


class OrderCreateForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['email', 'phone', 'fax', 'address', 'city', 'postal_code', 'country']
        widgets = {
            'email': forms.EmailInput(attrs={'required': True}),
            'phone': forms.TextInput(attrs={'required': True}),
            'address': forms.TextInput(attrs={'required': True}),
            'city': forms.TextInput(attrs={'required': True}),
            'postal_code': forms.TextInput(attrs={'required': True}),
            'country': forms.TextInput(attrs={'required': True}),
            'fax': forms.TextInput(attrs={'required': False}),
        }
