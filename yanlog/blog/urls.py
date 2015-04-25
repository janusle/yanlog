from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.IndexView.as_view(), name='index'),
    url(r'(?P<pk>[0-9]+)/$', views.PostView.as_view(), name='post'),
]
