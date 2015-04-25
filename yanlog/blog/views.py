from django.shortcuts import render
from django.views.generic import ListView, DetailView
from django.http import Http404

from .models import Post, Category, Tag

class IndexView(ListView):
    template_name = "index.html"
    model = Post

    def get_queryset(self):
        queryset = super(IndexView, self).get_queryset()
        # Only diplay English post in the IndexView
        return queryset.filter(lang='en')

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        categories = Category.objects.all()
        tags = Tag.objects.all()
        context.update({
            'categories': categories,
            'tags': tags
        })
        return context


class PostView(DetailView):
    model = Post
    template_name = 'post.html' 
