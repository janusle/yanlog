from django.db import models

class Page(models.Model):
	name = models.CharField(max_length=128)
	link = models.URLField()
	is_display_on_home = models.BooleanField(Default=False)
    
class Setting(models.Model):
    avatar = models.ImageField()


