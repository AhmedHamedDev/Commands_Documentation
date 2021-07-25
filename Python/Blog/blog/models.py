import blog
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.utils.text import slugify

class Blog(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    date = models.DateTimeField(auto_now_add=True)
    slug = models.SlugField(max_length=250, unique=False, blank=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_blogs')

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super(Blog, self).save(*args, **kwargs)



def blog_post_save_function(sender, instance, created, *args, **kwargs):
    if created and ~instance.slug.endswith(str(instance.id)):
        instance.slug += f"-{instance.id}"
        instance.save()
        

post_save.connect(blog_post_save_function, sender=Blog)

