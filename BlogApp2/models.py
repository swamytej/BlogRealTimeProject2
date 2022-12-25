from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.urls import reverse


# Create your models here.
class Custommanager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(status='Published')

from taggit.managers import TaggableManager
from django.core.validators import FileExtensionValidator


class Post(models.Model):
    STATUS_CHOICES =(('draft','Draft'),('published','Published'))
    title = models.CharField(max_length=250)
    slug = models.SlugField(max_length=264,unique_for_date='publish')
    author = models.ForeignKey(User,related_name='blog_posts',on_delete=models.CASCADE)
    body = models.TextField()
    publish =models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now= True)
    status = models.CharField(max_length=10,choices= STATUS_CHOICES,default='draft')
    images = models.FileField(null=True,blank=True,upload_to="images/",validators=[FileExtensionValidator(allowed_extensions= ['jpg','mp4','mp3','pdf','txt'])])
    objects= Custommanager()
    tags = TaggableManager()

    class Meta:
        ordering=('-publish',)
        def __str__(self):
            return self.title

    def get_absolute_url(self):
                return reverse('post_detail',args=[self.publish.year,self.publish.strftime('%m'),self.publish.strftime('%d'),self.slug])


class Comment(models.Model):
        post=models.ForeignKey(Post,related_name='comments',on_delete=models.CASCADE)
        name=models.CharField(max_length=32)
        email=models.EmailField()
        body=models.TextField(max_length=50)
        created=models.DateTimeField(auto_now_add=True)
        updated=models.DateTimeField(auto_now=True)
        active=models.BooleanField(default=True)
        class Meta:
            ordering=('created',)
        def __str__(self):
            return "Commented By {} on {}".format(self.name,self.post)

        def get_absolute_url(self):
            return reverse('detail', kwargs={'pk': self.pk})

