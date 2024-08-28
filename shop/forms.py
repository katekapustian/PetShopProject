from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Profile, Review


class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'password1', 'password2']

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('An account with this email already exists.')
        return email


class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['telephone', 'fax']


class AddressUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['address', 'city', 'zip_code', 'country']


class ReviewForm(forms.ModelForm):
    rating = forms.IntegerField(
        required=True,
        error_messages={
            'required': 'Please provide a rating for the product.'
        },
        widget=forms.RadioSelect()
    )

    class Meta:
        model = Review
        fields = ['first_name', 'last_name', 'email', 'rating', 'review_text']
        widgets = {
            'first_name': forms.TextInput(attrs={'placeholder': 'Name'}),
            'last_name': forms.TextInput(attrs={'placeholder': 'Last Name'}),
            'email': forms.EmailInput(attrs={'placeholder': 'Email'}),
            'review_text': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Message'}),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if user and user.is_authenticated:
            self.fields['first_name'].initial = user.first_name
            self.fields['last_name'].initial = user.last_name
            self.fields['email'].initial = user.email

    def clean_rating(self):
        rating = self.cleaned_data.get('rating')
        if not rating:
            raise forms.ValidationError('Please provide a rating for the product.')
        return rating
