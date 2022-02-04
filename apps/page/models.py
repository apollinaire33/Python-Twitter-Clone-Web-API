from django.db import models


class Tag(models.Model):
    name = models.CharField(max_length=30, unique=True)

    def __str__(self):
        return self.name


class Page(models.Model):
    name = models.CharField(max_length=80)
    uuid = models.CharField(max_length=30, unique=True)
    description = models.TextField(blank=True)
    tags = models.ManyToManyField('page.Tag', related_name='pages', blank=True)

    owner = models.ForeignKey('user.User', on_delete=models.CASCADE, related_name='pages')
    followers = models.ManyToManyField('user.User', related_name='follows', blank=True)

    image = models.URLField(null=True, blank=True)

    is_private = models.BooleanField(default=False)
    follow_requests = models.ManyToManyField('user.User', related_name='requests', blank=True)

    is_blocked = models.BooleanField(default=False)
    unblock_date = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.name


class Post(models.Model):
    page = models.ForeignKey('page.Page', on_delete=models.CASCADE, related_name='posts')
    content = models.CharField(max_length=180)

    likes = models.ManyToManyField('page.Page', related_name='liked_posts', blank=True)

    reply_to = models.ForeignKey('page.Post', on_delete=models.SET_NULL, null=True, blank=True, related_name='replies')

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.content
