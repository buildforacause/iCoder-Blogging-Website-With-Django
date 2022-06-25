from django import forms
from .models import BlogPost
from ckeditor.fields import RichTextField


class BlogPostForm(forms.ModelForm):
    content = RichTextField()

    class Meta:
        model = BlogPost
        fields = (
            'title',
            'content',
        )
        labels = {
            'title': ('Blog Title'),
            'content': ('Write your BlogPost here!'),

        }
