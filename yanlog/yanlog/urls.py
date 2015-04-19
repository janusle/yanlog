from django.conf.urls import include, url
from django.contrib import admin
from common import views as common_view

urlpatterns = [
    # Examples:
    # url(r'^$', 'yanlog.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', common_view.HomeView.as_view()),
    url(r'^blog/', include('blog.urls')),
]
