
from django.conf.urls import url, include
from rest_framework import routers
from framework_test import views
# BlogList, BlogKind, BlogListViewSet, BlogKindViewSet
router = routers.DefaultRouter()
router.register(r'bloglist', views.BlogListViewSet)
router.register(r'blogkind', views.BlogKindViewSet)
router.register(r'snippet', views.SnippetViewSet)

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.

urlpatterns = [
    url('', include(router.urls)),
    url('snippets', views.SnippetListInGeneric.as_view()),
    url('snippet_detail/(\d+)/', views.SnippetDetailInGeneric.as_view()),
    url('api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]