from django.contrib import admin

# Register your models here.

from . import models

admin.site.register(models.userinfo)
admin.site.register(models.confirmString)