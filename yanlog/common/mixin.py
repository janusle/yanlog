from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.urlresolvers import reverse_lazy

from blog.models import Setting


class CommonLoginRequiredMixin(LoginRequiredMixin):
    login_url = reverse_lazy('blog:login')


class LoadSettingsMixin(object):
    '''
    Load blog settings and insert them into context
    '''

    def get_context_data(self, **kwargs):
        setting = Setting.objects.first()
        if setting is None:
            setting = Setting.objects.create(blog_title='')

        context = super(LoadSettingsMixin, self).get_context_data(**kwargs)
        context.update({
            'blog_title': setting.blog_title,
        })
        return context
