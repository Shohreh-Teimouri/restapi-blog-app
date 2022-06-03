from cgitb import text
from multiprocessing import AuthenticationError
from turtle import title
from django.conf import settings
from django.db import models
from django.forms import CharField
from django.utils import timezone

# Create your models here.


class Post(models.Model):
    title = models.CharField(max_length=250)
    text = models.TextField()
    auther = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_date = models.DateTimeField(default=timezone.now)
    published_date = models.DateTimeField(blank=True, null=True)
    # visit_count = models.IntegerField(default=0)
    # visitors = models.ManyToManyField(settings.AUTH_USER_MODEL,
    #                                  related_name='post_visitor',
    #                                  editable=False)

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def approved_comments(self):
        return self.comments.filter(approved_comment=True)

    def __str__(self):
        return self.title


class Comment(models.Model):
    post = models.ForeignKey(
        'blog.Post', on_delete=models.CASCADE, related_name='comments')
    auther = models.CharField(max_length=250)
    text = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)
    approved_comment = models.BooleanField(default=False)

    def approve(self):
        self.approved_comment = True
        self.save()

    def __str__(self):
        return self.text


class SiteAbout(models.Model):
    title = models.CharField(max_length=150)
    address = models.CharField(max_length=400)
    fax = models.CharField(max_length=50)
    email = models.EmailField(max_length=50)
    about_text = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.about_text


# class PostViewWithUniqueUser(models.Model):
#     post = models.ForeignKey(Post, related_name='post_views',
#                              on_delete=models.CASCADE)
#     user = models.ForeignKey(settings.AUTH_USER_MODEL,
#                              related_name='user_view', on_delete=models.CASCADE)


class PostView(models.Model):
    post = models.ForeignKey(Post, related_name='post_views',
                             on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             related_name='user_view', on_delete=models.CASCADE)
