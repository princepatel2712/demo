from django.contrib import admin
from django.contrib.auth.models import Group
from .models import *

admin.site.register(Post)
admin.site.register(Follow)
admin.site.register(Like)
admin.site.register(Comment)
admin.site.register(Dislike)
admin.site.unregister(Group)
