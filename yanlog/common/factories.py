import factory
from . import models

class PageFactory(factory.DjangoModelFactory):
    class Meta:
        model = models.Page

    name = factory.Sequence(lambda n: 'name%s' % n)
    link = factory.Sequence(lambda n: '/%s/' % n)
    is_display_on_home = False
