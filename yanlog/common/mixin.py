from braces.views import LoginRequiredMixin
from django.core.urlresolvers import reverse_lazy

class CommonLoginRequiredMixin(LoginRequiredMixin):
    login_url = reverse_lazy('accounts:login')
