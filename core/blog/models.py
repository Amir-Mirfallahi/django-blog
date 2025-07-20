from django.db import models
from django.urls import reverse

# Create your models here.
class Post(models.Model):
    """
    this is a class to define posts for blog app
    """

    author = models.ForeignKey("accounts.Profile", on_delete=models.CASCADE)
    image = models.ImageField(null=True, blank=True)
    title = models.CharField(max_length=250)
    slug = models.SlugField(max_length=250, unique=True)
    read_time = models.IntegerField(default=2)
    views = models.IntegerField(default=0)
    content = models.TextField()
    status = models.BooleanField()
    category = models.ForeignKey("Category", related_name="posts", on_delete=models.SET_NULL, null=True)

    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    published_date = models.DateTimeField()

    def __str__(self):
        return self.title

    def get_snippet(self):
        return self.content[0:5]

    def get_absolute_api_url(self):
        return reverse("blog:api-v1:post-detail", kwargs={"pk": self.pk})


class Category(models.Model):
    """
    this is a class to define categories for blog table
    """

    name = models.CharField(max_length=250)

    def __str__(self):
        return self.name
