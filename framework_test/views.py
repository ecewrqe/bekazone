from blog_backend.models import BlogList, BlogKind
from framework_test.models import Snippet
from rest_framework import viewsets
from framework_test.serializers import BlogListSerializer, BlogKindSerializer, BlogDetailSerializer,SnippetSerializer
from django.http import JsonResponse, HttpResponse
from django.http import Http404

from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from rest_framework.decorators import api_view, APIView
from rest_framework import generics, mixins

class BlogListViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = BlogList.objects.all()
    serializer_class = BlogListSerializer


class BlogKindViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = BlogKind.objects.all()
    serializer_class = BlogKindSerializer

# class SnippetViewSet(viewsets.ModelViewSet):
#     queryset = Snippet.objects.all()
#     serializer_class = SnippetSerializer

class BlogListView(APIView):
    def get(self, request):
        blog_list = BlogList.objects.all()
        serializer = BlogListSerializer(blog_list, many=True)
        return JsonResponse(serializer.data, safe=False)
    def post(self, request):
        data = JSONParser().parse(request)
        serializer = BlogListSerializer(data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=301)

class BlogView(APIView):
    def get(self, request):
        title = request.GET.get("title")
        blog_list = BlogList.objects.filter(title=title)
        serializer = BlogDetailSerializer(blog_list, many=True)
        return JsonResponse(serializer.data, safe=False)


"""
class style view
"""
class SnippetList(APIView):
    def get(self, request):
        snippets = Snippet.objects.all()
        serializer = SnippetSerializer(snippets, many=True)
        return JsonResponse(serializer.data, safe=False)
    def post(self, request):
        # JSONRender/JSONParser
        data = JSONParser().parse(request)
        serializer = SnippetSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.error, status=301)

