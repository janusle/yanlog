import factory

from . import models


class PageFactory(factory.DjangoModelFactory):
    class Meta:
        model = models.Page

    title = factory.Sequence(lambda n: 'name%s' % n)
    url = factory.Sequence(lambda n: '/%s/' % n)
    is_display_on_home = False


class SettingFactory(factory.DjangoModelFactory):
    class Meta:
        model = models.Setting

    github = "https://github.com/janusle"
    twitter = "https://twitter.com/janusle"
    linkedin = "https://au.linkedin.com/pub/yan-le/33/31b/2a"
