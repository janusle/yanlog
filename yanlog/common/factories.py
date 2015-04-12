import factory
from . import models

class PageFactory(factory.Factory):
    class Meta:
        model = models.Page

    name = factory.Sequence(lambda n: 'name%s' % n)
    links = "/%s/" % name
    is_display_on_home = False
