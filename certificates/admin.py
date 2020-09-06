from django.contrib import admin

# Register your models here.
from .models import certificate,font

admin.site.register(certificate)
admin.site.register(font)