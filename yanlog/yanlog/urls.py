from django.conf.urls import include, url

from blog.views import IndexView

urlpatterns = [

    url(r'^$', IndexView.as_view()),
    url(r'^blog/', include('blog.urls', namespace='blog', app_name='blog')),
    url(r'^common/',
        include('common.urls', namespace='common', app_name='common')),
]
