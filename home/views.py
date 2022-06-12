from django.shortcuts import render, redirect
from .models import Contact
from blog.models import BlogPost
from django.http import HttpResponseNotFound, HttpResponseRedirect
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout

# Create your views here.


def home(request):
    posts = BlogPost.objects.all().order_by('-views')[:4]
    context = {'posts': posts}
    return render(request, "home/home.html", context)


def contact(request):
    if request.method == "POST":
        name = request.POST.get("name", "")
        email = request.POST.get("email", "")
        phone = request.POST.get("phone", "")
        desc = request.POST.get("desc", "")
        new_contact = Contact(name=name, email=email, phone=phone, desc=desc)
        new_contact.save()
        messages.success(request, 'Your response has been received successfully!')
    return render(request, "home/contact.html")


def search(request):
    query = request.GET.get("search")
    if len(query) > 70:
        posts = []
    else:
        poststitle = BlogPost.objects.filter(title__icontains=query)
        postsauthor = BlogPost.objects.filter(author__icontains=query)
        postscontent = BlogPost.objects.filter(content__icontains=query)
        posts = poststitle.union(postsauthor, postscontent)
    if not posts:
        messages.warning(request, f"No blogs found for your query! Please refine it to get better results!")
    return render(request, "home/search.html", {'posts': posts, 'query': query})


def handleSignup(request):
    if request.method == "POST":
        username = request.POST.get("name", "")
        email = request.POST.get("email", "")
        password = request.POST.get("password", "")
        if not username.isalnum():
            messages.error(request, 'Your iCoder username must only contain letters and numbers!')
            return redirect("/")
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already taken!')
            return redirect("/")
        try:
            new_user = User.objects.create_user(username=username, email=email, password=password)
            new_user.save()
            messages.success(request, 'Your iCoder account has been created successfully! Login Now!')
        except:
            messages.error(request, 'Your iCoder username must be unique! Please sign up again.')
        return redirect("/")
    else:
        return HttpResponseNotFound("<h1>404 - Forbidden</h1>The requested URL is not allowed!")


def handleLogin(request):
    if request.method == "POST":
        username = request.POST.get("name", "")
        password = request.POST.get("password", "")
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, 'Logged in Successfully!')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        else:
            messages.error(request, 'Invalid credentials!')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    else:
        return HttpResponseNotFound("<h1>404 - Forbidden</h1>The requested URL is not allowed!")


def handleLogout(request):
    if request.method == "POST":
        logout(request)
        messages.success(request, 'Successfully Logged out!')
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
