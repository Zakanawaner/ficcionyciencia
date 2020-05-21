from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse


LABEL_CHOICES = (
       ('ficción','ficción'),
       ('ciencia','ciencia'),
)


class Post(models.Model):
    title = models.CharField(max_length=100)
    label = models.CharField(max_length=7, choices=LABEL_CHOICES, default='ficción')
    content = models.TextField()
    likes = models.ManyToManyField(User, related_name='post_likes', blank=True)
    date_posted = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('post-detail', kwargs={'pk': self.pk})

    def get_like_url(self):
        return reverse('like-toggle', kwargs={'pk': self.pk})

    def get_comment_url(self):
        return reverse('comment-post', kwargs={'pk': self.pk})


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    name = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    body = models.TextField()
    created_on = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ['-created_on']

    def __str__(self):
        return 'Comentado {} por {}'.format(self.body, self.name)
