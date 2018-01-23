from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^(?P<article_id>[0-9]+)/$', views.detail, name = 'article_detail'),
    url(r'^(?P<year>[0-9]{4})/(?P<month>[0-9]{2})/$', views.archive, name = 'article_archive'),
    url(r'^post_comment/$', views.post_comment, name = 'post_comment'),
    url('', views.index, name = 'article_list'),
]