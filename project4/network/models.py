from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    @property
    def get_posts(self):
        return self.post.all()

    @property 
    def getFollowers(self):
        followers = []
        for follower in self.followers.all():
            name = follower.follower.username
            followers.append(name)
        return followers
         
    @property
    def getFollowing(self):
        following = []
        for follower in self.following.all():
            name = follower.followed.username
            following.append(name)
        return following
    @property
    def get_comments(self):
        return self.comments.all().order_by("-date")
    @property
    def get_followers(self):
        return self.followers.all()
    @property
    def get_following(self):
        return self.following.all()
    @property
    def get_likes(self): 
        return self.liked.all().order_by("-date")
    
    
    


class Posts(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="post")
    content = models.CharField(max_length=400, null=False)
    date = models.DateTimeField(auto_now_add=True)
    likes = models.IntegerField(null=False, default=0)

   
    @property
    def liked_users(self):
       likers = []
       for like in self.liked.all():
         name = like.owner.username 
         likers.append(name)
       return likers
    @property
    def get_likes(self):
        return self.liked.count()
    
    
class Comments(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comments")
    post = models.ForeignKey(Posts, on_delete=models.CASCADE, related_name="comments")
    comment = models.CharField(max_length=400, null=False)
    date = models.DateTimeField (auto_now_add=True)

class Liked(models.Model):
    post = models.ForeignKey(Posts, on_delete=models.CASCADE, related_name="liked")
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="liked" )
    likes = models.BooleanField(default=True)
    date = models.DateTimeField(auto_now_add=True)  

class Following(models.Model):
    follower = models.ForeignKey(User, on_delete=models.CASCADE, related_name="following")
    followed = models.ForeignKey(User, on_delete=models.CASCADE, related_name="followers")


