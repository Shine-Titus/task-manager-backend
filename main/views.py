from rest_framework.generics import ListAPIView,CreateAPIView,RetrieveUpdateDestroyAPIView
from .serializers import TaskSerializer ,RegisterSerializer
from .models import TasksModel, User, TaskSummary
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status, filters
from rest_framework.decorators import api_view, permission_classes, APIView
from django.shortcuts import get_object_or_404
from django.conf import settings
from openai import OpenAI

# Create your views here.
class ListTaskView(ListAPIView):
    queryset = TasksModel.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.SearchFilter]
    search_fields = ['title']
    
    def get_queryset(self):
        return TasksModel.objects.filter(user=self.request.user)
    
    def list(self, request, *args, **kwargs):

        response = super().list(request, *args, **kwargs) 
        return Response ({
            "user": {
                "id": request.user.id,
                "username": request.user.username,
                "email": request.user.email,
            },
            "tasks": response.data
        })

class CreateTaskView(CreateAPIView):
    queryset = TasksModel.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]

class ShowOrDeleteOrUpdateView(RetrieveUpdateDestroyAPIView):
    queryset = TasksModel.objects.all()
    serializer_class = TaskSerializer
    lookup_field = 'pk'
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return TasksModel.objects.filter(user=self.request.user)

class RegisterView(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer

    
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def mark_completed(request, pk):
    task = get_object_or_404(TasksModel, pk=pk, user=request.user)
    task.completed = not task.completed
    task.save()

    serializer = TaskSerializer(task, many=False)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def summarize_tasks(request):

    tasks = list(TasksModel.objects.filter(user=request.user, completed=False).values_list('title', flat=True))

    input_text = "Summarize the following tasks in a short paragraph, give tips on how to finish them:\n" + "\n".join(tasks)

    if not tasks:
        return Response({"summary": "No tasks to summarize!"})


    # OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    client = OpenAI(api_key=settings.OPENAI_API_KEY)

    response = client.responses.create(
      model="gpt-4o-mini",
      input=input_text,
      store=True,
    )

    summary_obj, created = TaskSummary.objects.update_or_create(
        user = request.user,
        defaults= {'summary' : response.output_text}
    )

    return Response({'summary': summary_obj.summary})



