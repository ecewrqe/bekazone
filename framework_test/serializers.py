from blog_backend.models import BlogList, BlogKind
from rest_framework import serializers
from framework_test.models import Snippet, LANGUAGE_CHOICES, STYLE_CHOICES

from django.http import JsonResponse, HttpResponse
# serialize連載, serial連続的、seriesシリーズ、
class BlogListSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = BlogList
        fields = ('title', )

class BlogKindSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = BlogKind
        fields = ('name', 'alias', 'introdution')

class SnippetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Snippet
        fields = ('id', 'title', 'code', 'linenos', 'language', 'style')

#class SnippetSerializer(serializers.Serializer):
#    id = serializers.IntegerField(read_only=True)
#    title = serializers.CharField(required=False, allow_blank=True, max_length=100)
#    code = serializers.CharField()
#    linenos = serializers.BooleanField(required=False)
#    language = serializers.ChoiceField(choices=LANGUAGE_CHOICES, default="python")
#    style = serializers.ChoiceField(choices=STYLE_CHOICES, default="friendly")

#    def create(self, validated_data):
#        """
#        create and return a new Snipped instance , given a validated data
#        """
#        return Snippet.objects.create(**validated_data)
    
#    def update(self, instance, validated_data):
#        """
#        update a new snipped instance
#        """
#        instance.title = validated_data.get('title', instance.title)
#        instance.code = validated_data.get('code', instance.code)
#        instance.linenos = validated_data.get('linenos', instance.linenos)
#        instance.language = validated_data.get('language', instance.language)
#        instance.style = validated_data.get('style', instance.style)
#        instance.save()
#        return instance