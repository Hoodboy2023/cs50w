from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse
from .models import User, Comments, Posts, Liked, Following
from django.views.decorators.csrf import csrf_exempt
import json
from django.core.paginator import Paginator

def index(request):
    if request.method == "GET": 
        posts = Posts.objects.all().order_by("-date")
        return render(request, "network/index.html", {"posts":posts})
    return HttpResponseRedirect(reverse("index"))
@login_required
def post(request, post_id):
    if request.method == "GET":
        try:
            post = Posts.objects.get(pk=post_id)
            comments = post.comments.all()
            return render(request, "network/post.html", {"post": post,"comments":comments})
        except:
            pass
    return HttpResponseRedirect(reverse("index"))

@login_required   
def profile(request, username):
    if request.method == "GET":
        try:
            user = User.objects.get(username=username)
            return render(request, "network/profile.html",{"userr": user })
        except:
            pass  
    return render(request, "network/profile.html",{"userr": user })

@login_required
def users(request):
    if request.method == "GET":
        users = User.objects.exclude(id=request.user.id)
        return render(request, "network/users.html", {"users": users}) 
    return HttpResponseRedirect(reverse("index"))

def notFound(request,exception):
    return render(request, "network/404.html", status=404)

def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password." 
            })
    else:
        return render(request, "network/login.html")

@login_required
def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")
@login_required  
def posts(request):
    if request.method == "POST":
        content = request.POST["content"]
        if content:
            post = Posts(owner=request.user, content=content)
            post.save()
        return HttpResponseRedirect(reverse("index"))
    return HttpResponseRedirect(reverse("index"))

@login_required    
@csrf_exempt
def comments(request, post_id):
    if request.method == "POST":
        post = Posts.objects.get(pk=post_id)
        data = json.loads(request.body)
        content = data.get("comment")
        if content and post:
            comment = Comments(owner=request.user, comment=content, post=post)
            comment.save()
            return JsonResponse({"message": "Comment added successfully"}, status=200)
    return  JsonResponse({"error": "Error"}, status=405)  

@login_required
@csrf_exempt
def likes(request, post_id):
    if request.method == "POST": 
        data = json.loads(request.body)
        liked = data["liked"]
        try:
            post = Posts.objects.get(pk=post_id)
        except:
            return JsonResponse({"message": "Error"})
        if liked == True and post:
            is_liked = Liked.objects.filter(post=post, owner=request.user)
            if not is_liked:
                like = Liked(post=post, owner=request.user)
                like.save()
                post.likes += 1
                post.save()
                return JsonResponse({"message": "Like added Successfully"}, status=200)
            else:
                return JsonResponse({"message": "Already liked"}, status=400)
           
        elif liked == False and post: 
            liked_post = Liked.objects.filter(post=post, owner=request.user)
            if liked_post:
                liked_post.delete()
                post.likes -= 1
                post.save()
                return JsonResponse({"message": "Like Removed"}, status=200)
            else:
                return JsonResponse({"message": "Error1"}, status=400) 
        print(liked, post)    
        return JsonResponse({"message": "error2"})     
    return JsonResponse({"message: error3"}, status=405)

@login_required
@csrf_exempt
def post_comments(request,):
    if request.method == "POST":
        data = json.loads(request.body)
        post_id = data["post_id"]
        if post_id:
           try:
               post = Posts.objects.get(pk=post_id)
           except:
               return JsonResponse({"message": "Error"}, status=400)
           comments = post.comments.all().order_by("-date") 
           data_list = []
           for comment in comments:
               data = {
                   "owner": comment.owner.username,
                   "comment": comment.comment,
                   "date": str(comment.date.strftime('%Y-%m-%d %H:%M'))
               }
               data_list.append(data)
           print(data_list)   
           return JsonResponse(data_list,safe=False, status=200) 
    return JsonResponse({"message": "error"}, status=405)       

@login_required
@csrf_exempt
def following(request, username):
    if request.method == "POST":
        try:
            user= User.objects.get(username=username)
        except:
            return JsonResponse({"message":"User does not exist"})
        is_follow_object = Following.objects.filter(followed=user, follower=request.user)
        if not is_follow_object:
            follow_oject = Following(follower=request.user, followed=user)
            follow_oject.save()
            return JsonResponse({"message": "User successfully followed"}, status=200)
        else:
            is_follow_object.delete()
            return JsonResponse({"message": "User successfully unfollowed"}, status=200)
    return JsonResponse({"message": "Error"}, status=200)    













