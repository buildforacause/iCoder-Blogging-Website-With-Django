from django.contrib import admin
from .models import BlogPost, Comment
# Register your models here.

admin.site.register((BlogPost, Comment))
