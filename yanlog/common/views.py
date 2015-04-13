from django.shortcuts import render
from django.views.generic import TemplateView
from .models import Page

class HomeView(TemplateView):
    template_name = "home.html"

    def get_context_data(self, **kwargs):
        context = super(HomeView, self).get_context_data(**kwargs)
        links = Page.objects.filter(is_display_on_home=True).values_list('link',
                    flat=True)
        context["links"] = links
        return context
