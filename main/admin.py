from django.contrib import admin
from .models import TasksModel, TaskSummary

# Register your models here.
admin.site.register(TasksModel)
admin.site.register(TaskSummary)