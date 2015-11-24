from django.conf.urls import include, url
from django.contrib import admin

from blog.views import IndexView

urlpatterns = [

    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', IndexView.as_view()),
    url(r'^blog/', include('blog.urls', namespace='blog', app_name='blog')),
    url(r'^common/',
        include('common.urls', namespace='common', app_name='common')),
    url(r'^accounts/',
        include('accounts.urls', namespace='accounts', app_name='accounts')),
]
