from django.urls import path
from . import views

urlpatterns = [
    path('', views.blogHome, name="BlogHome"),
    path('postsby_<author>/', views.filterAuthor, name="AuthorWisePosts"),
    path('newpost/', views.createPost, name="CreatePost"),
    path('editpost/<slug>/', views.editPost, name="EditPost"),
    path('postComment/', views.postComment, name="postComment"),
    path('editComment/<int:cid>/', views.editComment, name="editComment"),
    path('<slug>/', views.blogPost, name="BlogPost"),

]

