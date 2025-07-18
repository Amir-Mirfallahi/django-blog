from django.db import models
from blog.models import Post


class Comment(models.Model):
    """
    This is the comment model for managing comments of each post
    """
    message = models.TextField(max_length=500)
    reply_to = models.ForeignKey("self", related_name='replies', on_delete=models.CASCADE, null=True, blank=True)
    email = models.EmailField()
    name = models.CharField(max_length=250)
    post = models.ForeignKey(Post, related_name="comments", on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name}:{self.email} | {self.message[:25]}"
