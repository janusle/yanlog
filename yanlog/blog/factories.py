import factory
from . import models

class CategoryFactory(factory.DjangoModelFactory):
    class Meta:
        model = models.Category

    name = factory.Sequence(lambda n: 'Category%d' % n)


class TagFactory(factory.DjangoModelFactory):
    class Meta:
        model = models.Tag

    name = factory.Sequence(lambda n: 'Tag%d' % n)


class PostFactory(factory.DjangoModelFactory):
    class Meta:
        model = models.Post

    title = factory.Sequence(lambda n: 'Post%d' % n)
    content = "content"
    category = factory.SubFactory(CategoryFactory)

    @factory.post_generation
    def tags(self, create, extracted, **kwargs):
        if not create:
            return

        if extracted:
            for tag in extracted:
                self.tags.add(tag)
