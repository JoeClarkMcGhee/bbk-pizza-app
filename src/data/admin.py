from django.contrib import admin

from . import models

admin.site.register(models.Posts)
admin.site.register(models.Reactions)
admin.site.register(models.Topics)
