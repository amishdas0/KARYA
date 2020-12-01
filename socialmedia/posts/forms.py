from django.contrib.auth.forms import UserCreationForm

from django import forms
from .models import Post, Comment


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('caption', 'picture')


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('comment',)


class AddCommentForm(forms.Form):
    comment_field = forms.TextInput()
