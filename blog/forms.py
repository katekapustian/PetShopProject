from django import forms
from .models import Comment


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['author_name', 'author_email', 'content']
        widgets = {
            'content': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Message'}),
            'author_name': forms.TextInput(attrs={'placeholder': 'First Name'}),
            'author_email': forms.EmailInput(attrs={'placeholder': 'Email'}),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if user and user.is_authenticated:
            self.fields['author_name'].initial = user.first_name
            self.fields['author_email'].initial = user.email
            self.fields['author_name'].widget.attrs['readonly'] = True
            self.fields['author_email'].widget.attrs['readonly'] = True
            self.fields['author_name'].required = False
            self.fields['author_email'].required = False
        else:
            self.fields['author_name'].required = True
            self.fields['author_email'].required = True
