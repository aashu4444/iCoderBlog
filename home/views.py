from django.shortcuts import render, HttpResponse, redirect
from home.models import Contact
from django.contrib import messages
from blog.models import Post
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout


# Create your views here.
def home(request):
    return render(request, "home/home.html")

def contact(request):
    if request.method == 'POST':
        name = request.POST.get("name")
        email = request.POST.get("email")
        content = request.POST.get("content")
        phone = request.POST.get("phone")

        contact = Contact(name=name, email=email, content=content, phone=phone)
        contact.save()

        messages.success(request, "Your form has been submitted successfully.")

    return render(request, "home/contact.html")

def about(request):
    return render(request, "home/about.html")


def search(request):
    params = {}
    if request.method == "GET":
        query = request.GET["query"]
        allPosts = Post.objects.filter(title__icontains=query)

        params["allPosts"] = allPosts
        params["query"] = query

    return render(request, "home/search.html", params)

def handleSignup(request):
    if request.method == "POST":
        # Get the post parameters
        username = request.POST["username"]
        first_name = request.POST["first_name"]
        last_name = request.POST["last_name"]
        email = request.POST["email"]
        password1 = request.POST["password1"]
        password2 = request.POST["password2"]


        # Create the user
        myuser = User.objects.create_user(username, email, password1)
        myuser.first_name = first_name
        myuser.last_name = last_name
        myuser.save()

        messages.success(request, "Your account has been successfully created.")

        return redirect("/")

    else:
        return HttpResponse("404 not found.")

def handleLogin(request):
    if request.method == "POST":
        loginUsername = request.POST["loginUsername"]
        loginPassword = request.POST["loginPassword"]

        user = authenticate(username=loginUsername, password=loginPassword)

        if user is not None:
            login(request, user)
            messages.success(request, "Successfully Logged in.")
            return redirect("/")

        else:
            messages.error(request, "Please enter valid credentials")
            return redirect("/")


def handleLogout(request):
    logout(request)

    messages.success(request, "Successfully Logged out.")
    return redirect("/")
