from django.conf.urls import url
from blog_backend import views

urlpatterns = [
    url('^edit-blog/$', views.edit_blog, name='edit_blog'),
    url('^message/$', views.message, name='message'),
    url('^normal-edit-blog/$', views.normal_edit_blog, name='normal_edit_blog'),
    url('^md-edit-blog/$', views.md_edit_blog, name='md_edit_blog'),
    url('^display-blog-list/$', views.display_blog_list, name='display_blog_list'),
    url('^message-list/$', views.message_list, name='message_list'),
    url('^kind-list/$', views.kind_list, name='kind_list'),
    url('^kind-delete/$', views.kind_delete, name='kind_delete'),
    url('^verify-kind/$', views.kind_verify, name='verify_kind'),
    url('^tag-list/$', views.tag_list, name='tag_list'),
    url('^verify-tag/$', views.tag_verify, name='verify_tag'),
    url('^tag-delete/$', views.tag_delete, name='tag_delete'),
    url('^blog-title-verify/$', views.blog_title_verify, name='blog_title_verify'),
    url('^blog-delete/$', views.blog_delete, name='blog_delete'),
    url('^verify-related/$', views.verify_related, name="verify_related"),
    url('^get-blog-message/$', views.get_blog_message, name='get_blog_message'),
    url('^blog-view/$', views.blog_view, name='blog_view'),
    url('^upload-markdown/$', views.upload_markdown, name='upload_markdown'),
]
