from django.db import models
from django.contrib.auth.models import User
from imagekit.models import ProcessedImageField
from imagekit.processors import ResizeToFill


class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    caption = models.TextField(max_length=100, blank=False)
    picture = ProcessedImageField(upload_to='post_images',
                                  processors=[ResizeToFill(400, 400)],
                                  format='JPEG',
                                  options={'quality': 100})
    comments = models.ManyToManyField("Comment")


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.TextField(max_length=100, blank=False)
