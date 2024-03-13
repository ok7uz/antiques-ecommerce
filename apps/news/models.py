import uuid
from django.db import models
from ckeditor_uploader.fields import RichTextUploadingField


class News(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=255)
    subtitle = models.CharField(max_length=255)
    content = RichTextUploadingField()
    image = models.ImageField(upload_to='news/')
    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['date']
        verbose_name = 'news'
        verbose_name_plural = 'news'

    def __str__(self):
        return self.title
