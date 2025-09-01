from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.
class TasksModel(models.Model):

    title = models.CharField(max_length=200)
    completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    due_date = models.DateTimeField()
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='User')

    def __str__(self):
        return self.title
    
class TaskSummary(models.Model):
     
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    summary = models.TextField(blank=True,null=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.summary

