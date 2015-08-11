from django.shortcuts import render
from django.views.generic import FormView, View
from django.core.urlresolvers import reverse_lazy
from .models import Page, Setting
from .forms import LoginForm

class DashBoardView(View):
    pass

class LoginView(FormView):
    template_name = 'login.html'
    form_class = LoginForm
    success_url = reverse_lazy('common:dashboard')
