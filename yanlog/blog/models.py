from django.db import models

class Post(models.Model):
    title = models.CharField(max_length=100, blank=True)
    lang = models.CharField(max_length=2)
    content = models.TextField(blank=True)
    created_at = models.DateField()
    category = models.ForeignKey('Category')
    tags = models.ManyToManyField('Tag')


class Category(models.Model):
    name = models.CharField(max_length=100)


class Tag(models.Model):
    name = models.CharField(max_length=100)
