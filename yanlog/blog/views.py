from django import forms
from django.core.urlresolvers import reverse_lazy
from django.contrib import messages
from django.db.models import Count
from django.contrib.flatpages.models import FlatPage
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
        self.tag = self.request.GET.get('tag', None)
        self.year = self.request.GET.get('year', None)
        return super(IndexView, self).dispatch(request, *args, **kwargs)

    def get_queryset(self):
        queryset = super(IndexView, self).get_queryset()
        if self.tag:
            queryset = queryset.filter(tags__name=self.tag)
        if self.year:
            queryset = queryset.filter(created_at__year=self.year)
        return queryset

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        context.update({
            'tag': self.tag,
            'year': self.year,
        })
        return context


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


class PostAdminView(CommonLoginRequiredMixin, ListView):
    model = Post
    template_name = 'management/post.html'

    def get_context_data(self, **kwargs):
        context = super(PostAdminView, self).get_context_data(**kwargs)
        context.update({
            'post_management': True,  # for setting 'active' in top nav bar
        })
        return context


class PostView(DetailView):
    model = Post
    template_name = 'post/post.html'


class PostEditView(CommonLoginRequiredMixin):
    model = Post
    fields = ['title', 'created_at', 'content', 'tags']
    template_name = 'post/post_create_edit.html'

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

    def get_initial(self):
        return {'created_at': timezone.now()}


class PostUpdateView(PostEditView, UpdateView):
    action = 'Save'


class PostDeleteView(CommonLoginRequiredMixin, DeleteView):
    model = Post
    template_name = 'post/post_confirm_delete.html'
    success_url = reverse_lazy('blog:admin')


class TagAdminView(CommonLoginRequiredMixin, ListView):
    model = Tag
    template_name = 'management/tag.html'

    def get_context_data(self, **kwargs):
        context = super(TagAdminView, self).get_context_data(**kwargs)
        context.update({
            'tag_management': True,  # It's for setting 'active' in top nav bar
        })
        return context


class TagCUDBaseView(CommonLoginRequiredMixin):
    """
    BaseView for creating, updating and deleting tag
    """
    model = Tag
    http_method_names = [u'post']
    success_url = reverse_lazy('blog:tag_admin')
    fields = ['name']


class TagCreateView(TagCUDBaseView, CreateView):
    pass


class TagUpdateView(TagCUDBaseView, UpdateView):
    pass


class TagDeleteView(TagCUDBaseView, DeleteView):
    http_method_names = [u'post', u'delete']


class AboutUpdateView(CommonLoginRequiredMixin, UpdateView):
    model = FlatPage
    fields = ['content']
    template_name = 'management/about.html'
    success_url = reverse_lazy('blog:about_admin')

    def post(self, request, *args, **kwargs):
        # Add the flash message
        messages.success(request, "About page updated.")
        return super(AboutUpdateView, self).post(request, *args, **kwargs)

    def get_form(self, form_class=None):
        form = super(AboutUpdateView, self).get_form(form_class)
        form.fields['content'] = forms.fields.CharField(
            widget=MarkdownTextAreaWidget)
        return form

    def get_context_data(self, **kwargs):
        context = super(AboutUpdateView, self).get_context_data(**kwargs)
        context.update({
            'about_management': True,  # It's for setting 'active' in top nav bar
        })
        return context

    def get_object(self, queryset=None):
        about, _ = FlatPage.objects.get_or_create(title='about', url='/about/')
        # Make UpdateView always edit 'about' page
        self.kwargs[self.pk_url_kwarg] = about.id
        return super(AboutUpdateView, self).get_object(queryset)
