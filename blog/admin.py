from django.contrib import admin
from .models import Post, Comment
from .models import ToDo
from .models import Note

# Register your models here.

admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(ToDo)
admin.site.register(Note)