from django.conf.urls import url
from surl import views


urlpatterns = [
    url(r'^$', views.index_view, name='index'),
    url(r'^api/create/$', views.api_create_surl, name='api_create'),
    url(r'^create/$', views.create_surl_view, name='create'),
    url(r'^my/$', views.my_surl_view, name='my'),
    url(r'^(?P<slug>[a-zA-Z0-9_]{4,5})$', views.go_to_url, name='go'),
]
