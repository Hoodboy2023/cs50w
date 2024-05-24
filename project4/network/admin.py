from django.contrib import admin
from .models import Liked, Comments, Posts, Following
# Register your models here.
admin.site.register(Comments)
admin.site.register(Liked)
admin.site.register(Posts)
admin.site.register(Following) 