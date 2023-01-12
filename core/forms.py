from pyexpat import model
from re import A
from django import forms

from core.models import Post,Comment
from authentication.models import Profile

class ProfileForm(forms.ModelForm):

    class Meta:
        model = Profile
        fields = ['image','about']

class EditProfileForm(forms.ModelForm):

    class Meta:
        model = Profile
        fields = ['about']

class EditProfileImageForm(forms.ModelForm):
    image = forms.ImageField(widget=forms.FileInput())
    class Meta:
        model = Profile
        fields = ['image']

class PostForm(forms.ModelForm):
    content = forms.CharField(widget=forms.Textarea(attrs={"placeholder":"Content goes here ...."}))
    # image = forms.ImageField(widget=forms.FileInput())
    class Meta:
        model = Post
        fields = ('content','tag','image')

class CommentForm(forms.ModelForm):
    content = forms.CharField(widget=forms.Textarea(attrs={'placeholder':"Add a comment...","class":"comments","cols":"","rows":""}))
    # content = forms.CharField(widget=forms.TextInput(attrs={'placeholder':"Add a comment...","class":"comments","cols":"","rows":""}))
    class Meta:
        model = Comment
        fields = ['content']