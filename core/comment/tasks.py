from celery import shared_task
from django.utils import timezone
from .models import Comment
from blog.models import Post

@shared_task
def create_comment_task(post_id, reply_to_id, name, email, message):
    """
    Background task to create a new comment.
    """

    post = Post.objects.get(pk=post_id)
    parent = None
    if reply_to_id:
        try:
            parent = Comment.objects.get(pk=reply_to_id)
        except Comment.DoesNotExist:
            parent = None

    comment = Comment.objects.create(
        post=post,
        reply_to=parent,
        name=name,
        email=email,
        message=message,
    )
    return comment.id