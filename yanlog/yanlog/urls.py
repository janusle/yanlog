from django.conf.urls import include, url
from django.contrib import admin
from blog.views import IndexView
urlpatterns = [
    # Examples:
    # url(r'^$', 'yanlog.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', IndexView.as_view()),
    url(r'^blog/', include('blog.urls')),
    url(r'^common/', include('common.urls')),
]
