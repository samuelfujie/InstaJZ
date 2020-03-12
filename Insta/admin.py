from django.contrib import admin
from Insta.models import Post, InstaUser, Like, Comment, UserConnection

class CommentInLine(admin.StackedInline):
    model = Comment

class LikeInLine(admin.StackedInline):
    model = Like

class PostAdmin(admin.ModelAdmin):
    inlines = [
        CommentInLine,
        LikeInLine,
    ]

# Register your models here.
admin.site.register(Post, PostAdmin)
admin.site.register(InstaUser)
admin.site.register(Like)
admin.site.register(Comment)
admin.site.register(UserConnection)