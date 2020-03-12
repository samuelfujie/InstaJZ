from django.db import models
from django.urls import reverse
from django.contrib.auth.models import AbstractUser
from imagekit.models import ProcessedImageField

class InstaUser(AbstractUser):
    profile_pic = ProcessedImageField(
        upload_to='static/images/profiles',
        format='JPEG',
        options={'quality':100},
        blank=True,
        null=True,
    )

    def get_connections(self):
        connections = UserConnection.objects.filter(creator=self)
        return connections

    def get_followers(self):
        followers = UserConnection.objects.filter(following=self)
        return followers

    def is_followed_by(self, user):
        followers = UserConnection.objects.filter(following=self)
        return followers.filter(creator=user).exists()

class UserConnection(models.Model):
    # A follows B
    created = models.DateTimeField(auto_now_add=True, editable=False)
    # A
    creator = models.ForeignKey(
        InstaUser,
        on_delete=models.CASCADE,
        related_name="friendship_creator_set")
    # B
    following = models.ForeignKey(
        InstaUser,
        on_delete=models.CASCADE,
        related_name="friend_set")

    def __str__(self):
        return self.creator.username + ' |FOLLOWS| ' + self.following.username


class Post(models.Model):
    author = models.ForeignKey(InstaUser, on_delete=models.CASCADE, related_name='my_posts',)
    title = models.TextField(blank=True, null=True)
    image = ProcessedImageField(
        upload_to='static/images/posts',
        format='JPEG',
        options={'quality':100},
        blank=True,
        null=True,
    )
    posted_on = models.DateTimeField(auto_now_add=True, editable=False)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        """
        from django.core.urlresolvers import reverse
        """
        return reverse('post_detail', args=[self.id])
    
    def get_like_count(self):
        return self.likes.count()
    
    def get_comment_count(self):
        return self.comments.count()


class Like(models.Model):
    post = models.ForeignKey(
        Post,
        # if post is deleted, then the like is deleted as well
        on_delete=models.CASCADE,
        # post1.likes will return all likes belong to post1
        related_name='likes',
    )
    user = models.ForeignKey(
        InstaUser,
        on_delete=models.CASCADE,
        related_name='likes',
    )

    class Meta:
        # one post can only be liked by a user ONCE
        unique_together = ("post", "user")
    
    def __str__(self):
        return self.user.username + ' |LIKES| ' + self.post.title

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments',)
    user = models.ForeignKey(InstaUser, on_delete=models.CASCADE, related_name='comments',)
    comment = models.CharField(max_length=100)
    posted_on = models.DateTimeField(auto_now_add=True, editable=False)
    
    def __str__(self):
        return self.comment