from django.conf.urls import url, include
from bekazone.views import index, page_not_found

urlpatterns = [
    url(r'^$', index, name='index'),
    url('^users/', include('users.urls.web_urls', namespace='users')),
    url('^admin/', include('cadmin.urls', namespace='admin')),
    url('^blog-backend/', include('blog_backend.urls', namespace='blog_backend')),
    url('^framework-test/', include('framework_test.urls', namespace='framework_test')),
    
]

handler404 = page_not_found