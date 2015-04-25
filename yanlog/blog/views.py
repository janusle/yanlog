from django.shortcuts import render
from django.views.generic import ListView, DetailView
from django.http import Http404

from .models import Post, Category, Tag

class IndexView(ListView):
    template_name = "index.html"
    model = Post

    def dispatch(self, request, *args, **kwargs):
        year = kwargs.get('year', '') 
        month = kwargs.get('month', '') 
        if year:
            self.year = year 
        if month:
            self.month = month 
        return super(IndexView, self).dispatch(request, *args, **kwargs)

    def get_queryset(self):
        category = self.request.GET.get('category', None) 
        tag = self.request.GET.get('tag', None) 

        queryset = super(IndexView, self).get_queryset()
        if tag:
            queryset = queryset.filter(tags__name=tag)
        if category:
            queryset = queryset.filter(category__name=category)
        if hasattr(self, 'year') and hasattr(self, 'month'):
            queryset = queryset.filter(created_at__year=self.year, 
                                       created_at__month=self.month) 

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
