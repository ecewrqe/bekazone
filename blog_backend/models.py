from django.db import models
from users.models import User
# Create your models here.
class BlogList(models.Model):
    title = models.CharField(verbose_name="blog title", max_length=180, unique=True)
    creator = models.ForeignKey(to=User, related_name='u_b', null=True, blank=True, on_delete=models.CASCADE)
    blog_content = models.TextField(verbose_name="blog content", null=True, blank=True)
    md_content = models.TextField(verbose_name="markdown blog content", null=True, blank=True)
    blog_kind = models.ForeignKey("BlogKind", verbose_name="blog kind select", default=1, on_delete=models.CASCADE)
    tag = models.ManyToManyField("Tag", verbose_name="tag select")

    graphic_url = models.CharField(verbose_name="graphic url", max_length=180, null=True, blank=True)

    create_date = models.DateTimeField()
    adjustment_date = models.DateTimeField(null=True, blank=True)

class MessageList(models.Model):
    content = models.TextField(verbose_name="content", null=True, blank=True)
    creator = models.ForeignKey(to=User, related_name='u_m', null=True, blank=True, on_delete=models.CASCADE)
    create_date = models.DateTimeField()
    adjustment_date = models.DateTimeField(null=True, blank=True)

class BlogKind(models.Model):
    name = models.CharField(verbose_name="kind name", unique=True, max_length=32)
    alias = models.CharField(verbose_name="kind alias", unique=True, max_length=32, null=True, blank=True)
    introdution = models.TextField(verbose_name="introdution", null=True, blank=True)
    create_date = models.DateTimeField()

class Tag(models.Model):
    name = models.CharField(verbose_name="tag name", unique=True, max_length=32)