from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name = 'index'),
    url(r'^(?P<uid>[0-9]+)/follow/$', views.followlist, name='followlist'),
    url(r'^(?P<uid>[0-9]+)/follow/(?P<custid>[0-9]+)/$', views.follow, name='follow'),
    url(r'^(?P<uid>[0-9]+)/unfollow/(?P<custid>[0-9]+)/$', views.unfollow, name='unfollow'),
    url(r'^(?P<uid>[0-9]+)/followme/$', views.followme, name='followme'),
    url(r'^(?P<uid>[0-9]+)/comment/(?P<mid>[0-9]+)/$', views.comment, name='comment'),
    url(r'^(?P<uid>[0-9]+)/like$', views.like, name='like'),
    url(r'^(?P<uid>[0-9]+)/post$', views.post, name='post'),
    url(r'^(?P<uid>[0-9]+)/repost$', views.repost, name='repost'),
]

