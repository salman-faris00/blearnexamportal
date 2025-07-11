from django.contrib import admin


# Register your models here.

from .models import student  # replace with your model name

admin.site.register(student)
