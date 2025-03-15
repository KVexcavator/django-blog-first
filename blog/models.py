from django.conf import settings
from django.db import models
from django.urls import reverse
from django.utils import timezone
from mysite import settings

class PublishedManager(models.Manager):
  def get_queryset(self):
    return (
      super().get_queryset().filter(status=Post.Status.PUBLISHED)
    )

# in db table blog_post
class Post(models.Model):
  #enum
  class Status(models.TextChoices):
    DRAFT = 'DF', 'Draft'
    PUBLISHED = 'PB', 'Published'

  title = models.CharField(max_length=250)
  slug = models.SlugField(
    max_length=250,
    unique_for_date='publish'
    ) #short label
  # many-to-one
  author = models.ForeignKey(
    settings.AUTH_USER_MODEL,
    on_delete=models.CASCADE,
    related_name='blog_posts'
  )
  body = models.TextField()
  publish = models.DateTimeField(default=timezone.now)
  created = models.DateTimeField(auto_now_add=True)
  updated = models.DateTimeField(auto_now=True)
  status = models.CharField(
    max_length = 2,
    choices = Status,
    default = Status.DRAFT
  )
  objects = models.Manager() # The default manager.
  # Post.published.filter(title__startswith='Who')
  published = PublishedManager() # Our custom manager.

  class Meta:
    # default sort order
    ordering = ['-publish']
    #db index
    indexes = [
      models.Index(fields=['-publish'])
    ]

  #human-readable representation of the object
  def __str__(self):
    return self.title
  
  def get_absolute_url(self):
    return reverse(
      'blog:post_detail',
      args=[
        self.publish.year,
        self.publish.month,
        self.publish.day,
        self.slug
      ]
    )
