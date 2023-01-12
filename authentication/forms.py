from django.contrib.auth.models import User
from django import forms

from allauth.account.forms import SignupForm,LoginForm


class UserRegistrationForm(SignupForm):
    def __init__(self,*args,**kwargs):
        super(UserRegistrationForm,self).__init__(*args,**kwargs)
        self.fields['first_name'] = forms.CharField(required=True,widget=forms.TextInput(attrs={
            'placeholder': 'Firstname'
        }))
        self.fields['last_name'] = forms.CharField(required=True,widget=forms.TextInput(attrs={
            'placeholder': 'Lastname'
        }))

    def save(self,request):
        first_name = self.cleaned_data.pop('first_name')
        last_name = self.cleaned_data.pop('last_name')
        user = super(UserRegistrationForm,self).save(request)
        user.first_name = first_name
        user.last_name = last_name
        user.save()
        return user


