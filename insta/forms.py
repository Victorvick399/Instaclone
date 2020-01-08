from django import forms
from .models import Profile, Post, Comment
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


class ProfileForm(forms.ModelForm):
    '''
    class that defines how the update profile form will look like
    '''
    class Meta:
        model = Profile
        fields=['photo','bio']       
        exclude = ['user']


class UpdateUserForm(forms.ModelForm):
    '''
    class that defines how the update user form will look like
    '''
    class Meta:
        model = User
        fields = ['username']


class PostForm(forms.ModelForm):
    '''
    class that defines how the post form shall look like
    '''
    class Meta:
        model = Post
        exclude = ['posted_on', 'posted_by', 'likes', 'profile']

class CommentForm(forms.ModelForm):
  '''
  class that defines how the comment form shall look like
  '''
  class Meta:
    model= Comment
    exclude=['posted_on','image_id','posted_by']