from blog_backend.models import BlogList, BlogKind
from framework_test.models import Snippet
from rest_framework import viewsets
from framework_test.serializers import BlogListSerializer, BlogKindSerializer, SnippetSerializer
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

class SnippetViewSet(viewsets.ModelViewSet):
    queryset = Snippet.objects.all()
    serializer_class = SnippetSerializer

"""
class style view
"""
class SnippetList(APIView):
    def get(self, request):
        snippets = Snippet.objects.all()
        serializer = SnippetSerializer(snippets, many=True)
        return JsonResponse(serializer.data, safe=False)
    def post(self, request):
        data = JSONParser().parse(request)
        serializer = SnippetSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.error, status=301)

class SnippetListInGeneric(mixins.ListModelMixin, mixins.CreateModelMixin, generics.GenericAPIView):
    queryset = Snippet.objects.all()
    serialiser_class = SnippetSerializer
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)
    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)
class SnippetDetailInGeneric(mixins.RetrieveModelMixin, mixins.UpdateModelMixin, mixins.DestroyModelMixin, generics.GenericAPIView):
    queryset = Snippet.objects.all()
    serialiser_class = SnippetSerializer
    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.put(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.delete(request, *args, **kwargs)

class SnippetDetail(APIView):

    
    def get(self, request, pk):
        self.snippet = Snippet.objects.get(pk=pk)
        print(self.snippet)
        serializer = SnippetSerializer(self.snippet)
        return JsonResponse(serializer.data)
    def put(self, request, pk):
        self.snippet = Snippet.objects.get(pk=pk)
        data = JSONParser().parse(request)
        serializer = SnippetSerializer(self.snippet, data=data)
        if serializer.is_valid():
            serializer.save()
            
            return JsonResponse(serializer.data)
        return JsonResponse(serializer.erro, status=400)
    def delete(self, request, pk):
        self.snippet = Snippet.objects.get(pk=pk)
        self.snippet.delete()
        return HttpResponse(status=204)
"""
function style view
"""
@api_view(["GET"])
def snippet_list(request):
    print(request.data)
    if request.method == "GET":
        snippets = Snippet.objects.all()
        serializer = SnippetSerializer(snippets, many=True)
        return JsonResponse(serializer.data, safe=False)
    elif request.method == "POST":
        data = JSONParser().parse(request)
        serializer = SnippetSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.error, status=301)

def snippet_detail(request, pk):
    
    try:
        snippet = Snippet.objects.get(pk=pk)
    except Snippet.DoesNotExist:
        return HttpResponse(status=404)

    if request.method == "GET":
        serializer = SnippetSerializer(snippet)
        print(serializer.data)
        return JsonResponse(serializer.data)

    elif request.method == "PUT":
        data = JSONParser().parse(request)
        serializer = SnippetSerializer(snippet, data=data)
        if serializer.is_valid():
            serializer.save()
            
            return JsonResponse(serializer.data)
        return JsonResponse(serializer.erro, status=400)

    elif request.method == "DELETE":
        snippet.delete()
        return HttpResponse(status=204)