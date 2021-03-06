from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.urlresolvers import reverse_lazy


class CommonLoginRequiredMixin(LoginRequiredMixin):
    login_url = reverse_lazy('blog:login')
