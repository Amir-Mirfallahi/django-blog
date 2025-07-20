from django import forms
from .models import Post, Category

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = [
            "title", "slug", "read_time",
            "content", "status", "category", "published_date"
        ]
        widgets = {
            "title": forms.TextInput(attrs={
                "class": "w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-primary",
                "placeholder": "Enter post title"
            }),
            "slug": forms.TextInput(attrs={
                "class": "w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-primary",
                "placeholder": "unique-slug-for-url"
            }),
            "read_time": forms.NumberInput(attrs={
                "class": "w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-primary",
                "min": 1
            }),
            "views": forms.NumberInput(attrs={
                "class": "w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-primary",
                "min": 0
            }),
            "content": forms.Textarea(attrs={
                "class": "w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-primary prose prose-sm",
                "rows": 10,
                "placeholder": "Write the post content here..."
            }),
            "category": forms.Select(attrs={
                "class": "w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-primary"
            }),
            "published_date": forms.DateInput(format='%Y-%m-%d', attrs={
                "type": "date",
                "class": "w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-primary"
            }),
        }


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ("name",)
        widgets = {
            "name": forms.TextInput(attrs={
                    "class": "w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-primary",
                    "placeholder": "Enter category name."
                }),
        }