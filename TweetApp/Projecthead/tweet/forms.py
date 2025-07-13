from django import forms
from .models import Tweet, Comment, Message
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.models import User
#from django.conf import settings
#User = settings.AUTH_USER_MODEL
#from .models import CustomUser


class TweetForm(forms.ModelForm):
    class Meta:
        model = Tweet
        fields = ['text', 'photo']

class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField()
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text']
        widgets = {
            'text': forms.Textarea(attrs={'class': 'form-control', 'rows': 5, 'placeholder': 'Write your comment here...'}),
        }


class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Write your message here...'})
        }

# class UserRegistrationForm(UserCreationForm):
#     email = forms.EmailField()
#     class Meta:
#         model = CustomUser
#         fields = ('username', 'email', 'password1', 'password2')


# class CustomUserCreationForm(UserCreationForm):
#     class Meta:
#         model = CustomUser
#         fields = ('username', 'email', 'photo', 'bio')

# class CustomUserChangeForm(UserChangeForm):
#     class Meta:
#         model = CustomUser
#         fields = ('username', 'email', 'photo', 'bio')

