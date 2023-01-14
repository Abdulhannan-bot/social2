from django.forms import ModelForm, TextInput, EmailInput, PasswordInput
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout

from .models import *

from ckeditor.fields import RichTextField
from ckeditor_uploader.fields import RichTextUploadingField

class SignUpForm(UserCreationForm):
  username = forms.CharField(max_length = 100, required = True, widget = forms.TextInput(attrs = {'class': "form-control"}))
  first_name = forms.CharField(max_length = 30, required = True, widget = forms.TextInput(attrs = {'class': "form-control"}))
  last_name = forms.CharField(max_length = 30, required = True, widget = forms.TextInput(attrs = {'class': "form-control"}))
  email = forms.EmailField(max_length = 224, widget = forms.EmailInput(attrs = {'class': "form-control"}))
  password1 = forms.CharField(max_length = 20, required = True, widget = forms.PasswordInput(attrs = {'class': "form-control"}))
  password2 = forms.CharField(max_length = 20, required = True, widget = forms.PasswordInput(attrs = {'class': "form-control"}))

  class Meta:
    model = User
    fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']

class AccountForm(ModelForm):
  full_name = forms.CharField(max_length = 100, required = False, widget = forms.TextInput(attrs = {'class': "form-control"}))
  email = forms.EmailField(max_length = 224, required = False, widget = forms.TextInput(attrs = {'class': "form-control"}))
  profile_pic = forms.ImageField(widget = forms.FileInput(attrs = {'class': "form-control"}))
  class Meta:
    model = Account
    fields = ['full_name', 'email', 'profile_pic']

class PostForm(ModelForm):
  # post = forms.Textarea(widget = forms.Textarea(attrs = {'class': "form-control"}))
  class Meta:
    model = Post
    fields = ['post']

    widgets = {
      'post': forms.Textarea(attrs = {'class': "form-control"}),
    }

class CommentForm(ModelForm):
  class Meta:
    model = Comment
    fields = '__all__'
    exclude = ['created_at']

class SearchForm(ModelForm):
  username = forms.CharField(max_length = 100, required = False, widget = forms.TextInput(attrs = {'class': "form-control"}))
    