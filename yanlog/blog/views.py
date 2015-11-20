from django.shortcuts import render
from django.views.generic import (ListView, DetailView,
                                  UpdateView, CreateView, DeleteView)
from django.http import Http404
from django import forms
from django.core.urlresolvers import reverse_lazy

from common.mixin import CommonLoginRequiredMixin
from .utils import MarkdownTextAreaWidget
from .models import Post, Tag

class IndexView(ListView):
    template_name = "index.html"
    model = Post

    def dispatch(self, request, *args, **kwargs):
        tag = self.request.GET.get('tag', None)
        if tag:
            self.tag = tag
        return super(IndexView, self).dispatch(request, *args, **kwargs)

    def get_queryset(self):
        queryset = super(IndexView, self).get_queryset()
        if hasattr(self, 'tag'):
            queryset = queryset.filter(tags__name=self.tag)
        return queryset

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        tags = Tag.objects.all()
        context.update({
            'tags': tags
        })

        return context


class AdminView(CommonLoginRequiredMixin, IndexView):
    template_name = 'admin.html'


class PostView(DetailView):
    model = Post
    template_name = 'post/post.html'


class PostEditView(CommonLoginRequiredMixin):
    model = Post
    fields = ['title', 'content', 'tags']
    template_name = 'post/post_create_edit.html'

    def get_form(self, form_class=None):
        form = super(PostEditView, self).get_form(form_class)
        form.fields['content'] = forms.fields.CharField(widget=MarkdownTextAreaWidget)
        return form

    def get_context_data(self, **kwargs):
        context = super(PostEditView, self).get_context_data(**kwargs)
        context.update({
            'action': self.action
        })
        return context


class PostCreateView(PostEditView, CreateView):
    action = 'Create'


class PostUpdateView(PostEditView, UpdateView):
    action = 'Save'


class PostDeleteView(CommonLoginRequiredMixin, DeleteView):
    model = Post
    template_name = 'post/post_confirm_delete.html'
    success_url = reverse_lazy('blog:admin')
