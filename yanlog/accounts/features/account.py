from lettuce import before, after, step, world
from lettuce.django import django_url
from splinter import Browser

@before.all
def set_up():
    world.browser = Browser('chrome')


@step(r'I access the url \'([^\']*)\'')
def access_login(step, url):
    world.browser.visit(django_url(url))


@step(u'Then I see login page')
def then_i_see_login_page(step):
    u = world.browser.find_by_name('username')
    p = world.browser.find_by_name('password')
    assert len(u) != 0 and len(p) != 0


@after.all
def teardown(total):
    world.browser.quit()
