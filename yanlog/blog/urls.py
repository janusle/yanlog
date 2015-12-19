from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$',
        views.IndexView.as_view(),
        name='index'),
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
    url(r'archives/$',
        views.ArchiveView.as_view(),
        name='archives'),
]
