from django.shortcuts import render
from django.views.generic import FormView, View
from django.core.urlresolvers import reverse, reverse_lazy

from .models import Page, Setting
