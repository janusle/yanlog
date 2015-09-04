from django.shortcuts import render
from django.views.generic import ListView, DetailView
from django.http import Http404

from common.mixin import CommonLoginRequiredMixin


from .models import Post, Tag

class IndexView(ListView):
    template_name = "index.html"
    model = Post

    def dispatch(self, request, *args, **kwargs):
        year = kwargs.get('year', None)
        month = kwargs.get('month', None)
        tag = self.request.GET.get('tag', None)
        if year:
            self.year = year
        if month:
            self.month = month
        if tag:
            self.tag = tag
        return super(IndexView, self).dispatch(request, *args, **kwargs)

    def get_queryset(self):
        queryset = super(IndexView, self).get_queryset()
        if hasattr(self, 'tag'):
            queryset = queryset.filter(tags__name=self.tag)
        if hasattr(self, 'year') and hasattr(self, 'month'):
            queryset = queryset.filter(created_at__year=self.year,
                                       created_at__month=self.month)

        # Only diplay English post in the IndexView
        return queryset.filter(lang='en')

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        tags = Tag.objects.all()
        context.update({
            'tags': tags
        })
        return context


class AdminView(CommonLoginRequiredMixin, IndexView):
    template_name = 'admin.html'


class PostView(CommonLoginRequiredMixin, DetailView):
    model = Post
    template_name = 'post.html'
