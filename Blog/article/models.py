from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.db.models.signals import pre_save
from django.conf import settings
from Blog.utils import unique_slug_generator


class Article(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL,
                               on_delete=models.CASCADE,)

    title = models.CharField(max_length=120)
    created = models.DateTimeField(default=timezone.now)
    description = models.TextField(null=False)
    ingredient = models.TextField(null=False)

    image = models.ImageField(
        upload_to="images/",
        null=True, blank=True,
        width_field="width_field", height_field="height_field")
    height_field = models.IntegerField(default=0)
    width_field = models.IntegerField(default=0)

    slug = models.SlugField(max_length=50, unique=True)

    def __str__(self):
        return f'{self.title}'

    def get_absolute_detail_url(self):
        return reverse("article:article-detail", kwargs={"slug": self.slug})


# pre save slug receiver
def slug_save(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = unique_slug_generator(
            instance, instance.title, instance.slug)


pre_save.connect(slug_save, sender=Article)
