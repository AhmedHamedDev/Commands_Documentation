from django.contrib import admin
from . import models

# Register your models here.
admin.site.register(models.UserProfile)
admin.site.register(models.Question)
admin.site.register(models.Option)
