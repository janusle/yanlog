from django.db import models
from django.utils.encoding import python_2_unicode_compatible

@python_2_unicode_compatible
class Post(models.Model):
    title = models.CharField(max_length=100, blank=True)
    lang = models.CharField(max_length=2)
    content = models.TextField(blank=True)
    created_at = models.DateField()
    tags = models.ManyToManyField('Tag')

    def __str__(self):
        return self.title

@python_2_unicode_compatible
class Tag(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
    	return self.name
