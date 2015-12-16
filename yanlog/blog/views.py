from django import forms
from django.core.urlresolvers import reverse_lazy
from django.db.models import Count
from django.utils import timezone
from django.views.generic import (CreateView, DeleteView, DetailView, ListView,
                                  TemplateView, UpdateView)

from common.mixin import CommonLoginRequiredMixin

from .models import Post, Tag
from .utils import MarkdownTextAreaWidget


class IndexView(ListView):
    template_name = "index.html"
    model = Post

    def dispatch(self, request, *args, **kwargs):
        tag = self.request.GET.get('tag', None)
        year = self.request.GET.get('year', None)
        if tag:
            self.tag = tag
        if year:
            self.year = year
        return super(IndexView, self).dispatch(request, *args, **kwargs)

    def get_queryset(self):
        queryset = super(IndexView, self).get_queryset()
        if hasattr(self, 'tag'):
            queryset = queryset.filter(tags__name=self.tag)
        if hasattr(self, 'year'):
            queryset = queryset.filter(created_at__year=self.year)
        return queryset


class AdminView(CommonLoginRequiredMixin, IndexView):
    template_name = 'admin.html'


class PostView(DetailView):
    model = Post
    template_name = 'post/post.html'


class PostEditView(CommonLoginRequiredMixin):
    model = Post
    fields = ['title', 'content', 'created_at', 'tags']
    template_name = 'post/post_create_edit.html'

    def get_initial(self):
        return {'created_at': timezone.now() }

    def get_form(self, form_class=None):
        form = super(PostEditView, self).get_form(form_class)
        form.fields['content'] = forms.fields.CharField(
            widget=MarkdownTextAreaWidget)
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


class ArchiveView(TemplateView):
    template_name = 'archive.html'

    def get_context_data(self, **kwargs):
        context = super(ArchiveView, self).get_context_data(**kwargs)
        tags = (Tag.objects
                   .annotate(num_posts=Count('post'))
                   .values('name', 'num_posts'))
        years = (Post.objects
                     .extra(select={'year': 'to_char(created_at, \'YYYY\')'})
                     .values('year').order_by('year')
                     .annotate(num_posts=Count('id')))
        context.update({
            'tags': tags,
            'years': years,
        })
        return context
