from django.db import models
from django.contrib.auth.models import User
from ckeditor.fields import RichTextField
# Create your models here.


class BlogPost(models.Model):
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=125)
    content = RichTextField(blank=True, null=True)
    slug = models.CharField(max_length=250)
    views = models.IntegerField(default=0)
    timeStamp = models.DateTimeField(auto_now_add=True, blank=True)

    def __str__(self):
        return f'{self.title} - {self.author}'


class Comment(models.Model):
    content = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(BlogPost, on_delete=models.CASCADE)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True)
    timeStamp = models.DateTimeField(auto_now_add=True, blank=True)

    def __str__(self):
        return f'{self.content[0:13]} by {self.user.username}'
