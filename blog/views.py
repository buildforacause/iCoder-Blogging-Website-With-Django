from django.shortcuts import render, redirect
from .models import BlogPost, Comment
from django.contrib import messages
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
    if request.method == "POST":
        title = request.POST.get("title", "")
        author = request.POST.get("author", "")
        content = request.POST.get("content", "")
        slug = "-".join(title.split(" "))
        new_post = BlogPost(title=title,
                            author=author,
                            slug=slug,
                            content=content,
                            timeStamp=datetime.now(timezone.utc))
        new_post.save()
        messages.success(request, "Congratulations! Your new Blog has been published!!")
        return redirect("/blog/")
    return render(request, "blog/createpost.html", {'user': request.user})


def filterAuthor(request, author):
    posts = BlogPost.objects.filter(author=author)
    return render(request, "blog/authorwiseposts.html", {"posts": posts, 'author': author})


def editPost(request, slug):
    post = BlogPost.objects.filter(slug=slug).first()
    if request.method == "POST":
        post.title = request.POST.get("title", "")
        post.content = request.POST.get("content", "")
        post.save()
        return redirect(f"/blog/{post.slug}")
    return render(request, "blog/editblogpost.html", {'post': post})
