from django.conf.urls import url
from frontpage import views

urlpatterns = [
    url('^$', views.post_list, name='post_list'),
    url('^post-list/$', views.post_list, name='post_list'),
    url('^post-view/$', views.post_view, name='post_view'),
    ]