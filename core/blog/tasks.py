from celery import shared_task
from .models import Category
from django.db.models import Count


@shared_task
def remove_unused_categories():
    categories_to_remove = Category.objects.annotate(
        num_posts=Count('posts')
    ).filter(num_posts=0)
    categories_to_remove.delete()
    