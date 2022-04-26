from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
import uuid


class SignUpForm(UserCreationForm):
    email = forms.EmailField(label="", widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Email'}), )	

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2',)
        exclude = ('username',)

    def __init__(self, *args, **kwargs):
        super(SignUpForm, self).__init__(*args, **kwargs)

        

        self.fields['password1'].widget.attrs['class'] = 'form-control'
        self.fields['password1'].widget.attrs['placeholder'] = 'Mot de Passe'
        self.fields['password1'].label = ''
        self.fields['password1'].help_text = ''

        self.fields['password2'].widget.attrs['class'] = 'form-control'
        self.fields['password2'].widget.attrs['placeholder'] = 'Confirmez Votre Mot de Passe'
        self.fields['password2'].label = ''
        self.fields['password2'].help_text = ''