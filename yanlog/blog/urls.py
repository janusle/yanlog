from django.conf.urls import url
from django.contrib.auth import views as auth_views

from . import views

urlpatterns = [
    url(r'^$',
        views.IndexView.as_view(),
        name='index'),
    url(r'archives/$',
        views.ArchiveView.as_view(),
        name='archives'),
    url(r'^login/$', auth_views.login,
        {'template_name': 'login.html'},
        name='login'),
    url(r'^post/(?P<pk>[0-9]+)/$',
        views.PostView.as_view(),
        name='post'),
    url(r'^admin/$',
        views.PostAdminView.as_view(),
        name='admin'),
    url(r'post/(?P<pk>[0-9]+)/edit/$',
        views.PostUpdateView.as_view(),
        name='post_update'),
    url(r'post/(?P<pk>[0-9]+)/delete/$',
        views.PostDeleteView.as_view(),
        name='post_delete'),
    url(r'post/create/$',
        views.PostCreateView.as_view(),
        name='post_create'),
    url(r'tag/admin/$',
        views.TagAdminView.as_view(),
        name='tag_admin'),
    url(r'tag/(?P<pk>[0-9]+)/delete/$',
        views.TagDeleteView.as_view(),
        name='tag_delete'),
]
