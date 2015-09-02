from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.IndexView.as_view(), name='index'),
    url(r'^admin/$', views.AdminView.as_view(), name='admin_index'),
    url(r'(?P<year>[0-9]{4})/(?P<month>([1-9]|1[1-2]))/$', views.IndexView.as_view(), name='index'),
    url(r'(?P<pk>[0-9]+)/$', views.PostView.as_view(), name='post'),
]
