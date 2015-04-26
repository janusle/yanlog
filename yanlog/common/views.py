from django.shortcuts import render
from django.views.generic import TemplateView
from .models import Page, Setting

class HomeView(TemplateView):
    template_name = "home.html"

    def get_context_data(self, **kwargs):
        context = super(HomeView, self).get_context_data(**kwargs)
        urls = Page.objects.filter(is_display_on_home=True).values_list('url',
                    flat=True)
        context['urls'] = urls
        if Setting.objects.count():
            setting = Setting.objects.all()[0]
            context['github'] = setting.github
            context['twitter'] = setting.twitter
            context['linkedin'] = setting.linkedin
        return context
