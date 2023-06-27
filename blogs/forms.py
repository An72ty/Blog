from django import forms
from .models import BlogPost, Comment


class PostForm(forms.ModelForm):
    class Meta:
        model = BlogPost
        fields = ['title', 'text']
        labels = {'title': 'Title:', 'text': 'Text'}
        widgets = {'text': forms.Textarea(attrs={'cols': 80})}

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text']
        labels = {'text': ''}