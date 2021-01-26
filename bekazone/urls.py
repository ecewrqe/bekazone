from django.conf.urls import url, include
from bekazone.views import index
from bekazone.utils import page_not_found
from frontpage.views import index as frontpage_index


urlpatterns = [
    url(r'^backend/$', index, name='index'),
    url('^backend/users/', include(('users.urls.web_urls', 'users'), )),
    url('^backend/admin/', include(('cadmin.urls', 'admin'), )),
    url('^backend/blog-backend/', include(('blog_backend.urls', 'blog_backend'), )),
#    url('^backend/framework-test/', include(('framework_test.urls', 'framework_test'), )),
    url(r'^$', frontpage_index),
    url(r'^frontpage/', include(('frontpage.urls', 'frontpage'), )),
]

handler404 = page_not_found
