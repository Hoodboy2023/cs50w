
from django.urls import path
from django.conf.urls import handler404
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login/", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("posts", views.posts, name="posts"),
    path("comments/<int:post_id>", views.comments, name="comments"),
    path("like/<int:post_id>", views.likes, name="like"),
    path("post/<int:post_id>", views.post, name="post"),
    path("comments", views.post_comments, name="post_comments"),
    path("profile/<str:username>", views.profile, name="profile"),
    path("users", views.users, name="users"), 
    path("following/<str:username>", views.following, name="following")
]

