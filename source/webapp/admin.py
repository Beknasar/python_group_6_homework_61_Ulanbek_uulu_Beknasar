from django.contrib import admin
from .models import Tasks, Type, Status

admin.site.register(Tasks)
admin.site.register(Type)
admin.site.register(Status)