from markdown2 import markdown

from django import template
from django.template.defaultfilters import stringfilter
from django.utils.safestring import mark_safe


register = template.Library()

@register.filter
@stringfilter
def md(value):
    """ Parse the markdown and return html """
    return mark_safe(markdown(value, extras=['fenced-code-blocks']))
