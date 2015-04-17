from django.db import models
from django.contrib.flatpages.models import FlatPage

class Page(FlatPage):
	is_display_on_home = models.BooleanField(default=False)


class Setting(models.Model):
    avatar = models.ImageField()
