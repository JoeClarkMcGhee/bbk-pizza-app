from django.contrib import admin

from . import models

admin.site.register(models.Post)
admin.site.register(models.Reaction)
admin.site.register(models.Topics)
