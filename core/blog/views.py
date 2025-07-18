from django.views.generic import ListView, DetailView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import PostForm

from blog.models import Post, Category


class HomeView(ListView):
    template_name = "blog/home.html"
    paginate_by = 10

    def get_queryset(self):
        category_id = self.request.GET.get("category", "all")
        query = self.request.GET.get("query", "")
        if category_id != "all":
            posts = Post.objects.filter(title__icontains=query, content__icontains=query, category_id=category_id, status=True).order_by("-id")
        elif query:
            posts = Post.objects.filter(title__icontains=query, content__icontains=query, status=True).order_by("-id")
        else:
            posts = Post.objects.filter(status=True).order_by("-id")
        return posts

    def get_context_data(self, **kwargs):
        context = super(HomeView, self).get_context_data(**kwargs)
        context["categories"] = Category.objects.all()
        return context


class PostDetailView(DetailView):
    template_name = "blog/post-detail.html"
    context_object_name = "post"
    slug_url_kwarg = "slug"
    model = Post

    def get_context_data(self, **kwargs):
        context = super(PostDetailView, self).get_context_data(**kwargs)
        context["related_posts"] = Post.objects.filter(status=True).order_by("-id")[:3]
        post = context["post"]
        post.views += 1
        post.save()
        return context


class PostCreateView(LoginRequiredMixin, CreateView):
    form_class = PostForm
    model = Post
    template_name = "blog/post-create.html"
    success_url = "/"

    def form_valid(self, form):
        form.instance.author = self.request.user.profile
        return super().form_valid(form)
