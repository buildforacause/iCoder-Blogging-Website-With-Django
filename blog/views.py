from django.shortcuts import render, redirect
from .models import BlogPost, Comment
from django.contrib import messages
from .forms import BlogPostForm
from django.http import HttpResponseRedirect
from datetime import datetime, timezone
# Create your views here.


def blogHome(request):
    posts = BlogPost.objects.all()
    context = {'posts': posts}
    return render(request, "blog/bloghome.html", context)


def blogPost(request, slug):
    post = BlogPost.objects.filter(slug=slug).first()
    if request.user.is_authenticated:
        post.views += 1
        post.save()
    comments = Comment.objects.filter(post=post, parent=None)
    replies = Comment.objects.filter(post=post).exclude(parent=None)
    return render(request, "blog/post.html", {'post': post, 'comments': comments, 'replies': replies})


def postComment(request):
    if request.method == "POST":
        content = request.POST.get("content", "")
        postId = request.POST.get("postId", "")
        parentid = request.POST.get("commentId", "")
        post = BlogPost.objects.filter(id=postId).first()
        user = request.user
        if parentid:
            parent = Comment.objects.filter(id=parentid).first()
            comment = Comment(content=content, post=post, user=user, parent=parent)
        else:
            comment = Comment(content=content, post=post, user=user)
        comment.save()
        messages.success(request, "Your comment has been posted successfully!")
    return redirect(f"/blog/{post.slug}")


def editComment(request, cid):
    if request.method == "POST":
        comment = Comment.objects.filter(id=cid).first()
        comment.content = request.POST.get("content", "")
        comment.timeStamp = datetime.now(timezone.utc)
        comment.save()
        messages.success(request, "Your comment has been edited successfully!")
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def createPost(request):
    form = BlogPostForm()
    if request.method == "POST":
        form = BlogPostForm(request.POST)
        if form.is_valid():
            new_post = form.save(commit=False)
            new_post.author = request.user.username
            new_post.slug = "-".join(new_post.title.split(" "))
            new_post.timeStamp = datetime.now(timezone.utc)
            new_post.save()
            messages.success(request, "Congratulations! Your new Blog has been published!!")
            return redirect("/blog/")
    return render(request, "blog/createpost.html", {'user': request.user, 'form': form})


def filterAuthor(request, author):
    posts = BlogPost.objects.filter(author=author)
    return render(request, "blog/authorwiseposts.html", {"posts": posts, 'author': author})


def editPost(request, slug):
    post = BlogPost.objects.filter(slug=slug).first()
    form = BlogPostForm(instance=post)
    if request.method == "POST":
        form = BlogPostForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            messages.success(request, "You have successfully edited your BlogPost!")
        return redirect(f"/blog/{post.slug}")
    return render(request, "blog/editblogpost.html", {'post': post, 'form': form})
