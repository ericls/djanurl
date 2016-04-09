from django.conf.urls import url
from .views import index_view


urlpatterns = [
    url('^$', index_view, name='index')
]
