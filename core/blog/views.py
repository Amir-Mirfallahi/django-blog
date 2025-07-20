from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from .mixins import OwnerRequiredMixin
from django.shortcuts import get_object_or_404
from .forms import PostForm, CategoryForm
from django.urls import reverse_lazy
from django.db.models import Q

from blog.models import Post, Category


class HomeView(ListView):
    template_name = "blog/home.html"
    paginate_by = 12

    def get_queryset(self):
        qs = Post.objects.filter(status=True)

        # 1) Filter by category if set and valid
        category = self.request.GET.get("category")
        if category and category != "all":
            try:
                category_id = int(category)
                qs = qs.filter(category_id=category_id)
            except ValueError:
                # invalid category id in URL—ignore or log
                pass

        # 2) Filter by search query, matching title OR content
        query = self.request.GET.get("query", "").strip()
        if query:
            qs = qs.filter(
                Q(title__icontains=query) |
                Q(content__icontains=query)
            )

        # 3) Final ordering
        return qs.order_by("-id")

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
        context["categories"] = Category.objects.all()
        post = context["post"]
        post.views += 1
        post.save()
        return context


class PostCreateView(LoginRequiredMixin, CreateView):
    form_class = PostForm
    model = Post
    template_name = "blog/post-form.html"
    success_url = reverse_lazy("blog:post-list")

    def form_valid(self, form):
        form.instance.author = self.request.user.profile
        return super().form_valid(form)


class CategoryCreateView(LoginRequiredMixin, CreateView):
    model = Category
    form_class = CategoryForm
    template_name = "blog/category-create.html"
    success_url = "/create"


class PostListView(LoginRequiredMixin, ListView):
    model = Post
    template_name = "blog/post-list.html"

    def get_queryset(self):
        category_id = self.request.GET.get("category", "all")
        query = self.request.GET.get("query", "")
        if category_id != "all":
            posts = Post.objects.filter(title__icontains=query, content__icontains=query, category_id=category_id, author=self.request.user.profile).order_by("-id")
        elif query:
            posts = Post.objects.filter(title__icontains=query, content__icontains=query, author=self.request.user.profile).order_by("-id")
        else:
            posts = Post.objects.filter(author=self.request.user.profile).order_by("-id")
        return posts


class PostUpdateView(LoginRequiredMixin, OwnerRequiredMixin, UpdateView):
    model = Post
    template_name = "blog/post-form.html"
    form_class = PostForm
    success_url = "/posts"


class PostDeleteView(LoginRequiredMixin, OwnerRequiredMixin, DeleteView):
    model = Post
    template_name = "blog/post-remove.html"
    success_url = "/posts"