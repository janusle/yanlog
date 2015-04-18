from django.db import models

class Post(models.Model):
    title = models.CharField(max_length=100, blank=True)
    content = models.TextField(blank=True)
    created_at = models.DateField(auto_now_add=True)
    category = models.ForeignKey('Category')
    tags = models.ManyToMany('Tag')


class Cateogry(models.Model):
    name = models.CharField(max_length=100)


class Tag(models.Model):
    name = models.CharField(max_length=100)
