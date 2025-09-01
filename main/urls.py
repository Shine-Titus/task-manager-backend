from django.urls import path
from . import views

urlpatterns = [
    path('view-tasks/', views.ListTaskView.as_view(), name='tasks.view'),
    path('create-tasks/', views.CreateTaskView.as_view(), name='tasks.create'),
    path('view-tasks/<int:pk>/', views.ShowOrDeleteOrUpdateView.as_view(), name='task.showordeleteorupdate'),
    path('api/register/', views.RegisterView.as_view(), name='register'),
    path('view-tasks/<int:pk>/completed/', views.mark_completed, name='task.completed'),
    path('summarize-tasks/', views.summarize_tasks, name='task.summarize'),
]