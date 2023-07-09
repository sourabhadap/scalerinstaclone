from django import forms
from .models import User, UserProfile


class UserSignUp(forms.ModelForm):
    name = forms.CharField(max_length=100, required=True,
                           widget=forms.widgets.TextInput(attrs={'placeholder': 'Enter your name',
                                                                 'class': 'input-field'}),
                           label='Name',
                           error_messages={'required': 'Please enter your name'})
    email = forms.EmailField(max_length=100, required=True,
                             widget=forms.widgets.EmailInput(attrs={'placeholder': 'Enter your email',
                                                                    'class': 'input-field'})
                             , label='Email',
                             error_messages={'required': 'Please enter your email'})
    password = forms.CharField(max_length=100, required=True,
                               widget=forms.widgets.PasswordInput(attrs={'placeholder': 'Enter your password',
                                                                          'class': 'input-field'})
                               , label='Password',
                               error_messages={'required': 'Please enter your password'})

    class Meta:
        model = User
        exclude = ('is_active', 'created_on', 'updated_on','phone_number')
