from django.conf.urls import url
from django.contrib import admin
from cadmin import views

urlpatterns = [
    url(r'^(\w+)/(\w+)/add/$', views.table_add, name="table_add"),
    url(r'^(\w+)/(\w+)/(\d+)/change/$', views.table_change, name="table_change"),
    url(r'^(\w+)/(\w+)/(\d+)/delete/$', views.table_delete, name="table_delete"),
    url(r'^(\w+)/(\w+)/$', views.table_list, name="table_list"),
    url(r'^(\w+)/$', views.app_model, name="table_model_list"),
    url(r'^get-action/$', views.get_action, name="get_action"),
    url(r'^batch-update/$', views.batch_update, name="batch_update"),
    url(r'^$', views.index, name="index"),
]
