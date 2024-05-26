from django.contrib import admin
from .models import Liked, Comments, Posts, Following, User
# Register your models here.
admin.site.register(Comments)
admin.site.register(Liked)
admin.site.register(Posts)
admin.site.register(Following) 
admin.site.register(User) 

