from django.contrib.flatpages.models import FlatPage
from django.db import models


class Page(FlatPage):
	is_display_on_home = models.BooleanField(default=False)


class Setting(models.Model):
    avatar = models.ImageField(null=True, blank=True)
    github = models.URLField(null=True, blank=True)
    linkedin = models.URLField(null=True, blank=True)
    twitter = models.URLField(null=True, blank=True)
