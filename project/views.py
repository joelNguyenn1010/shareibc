from django.shortcuts import render
from rest_framework import generics,permissions
from .serializers import ProjectSerializer
from .models import Project
# Create your views here.


class ProjectsAPIView(generics.ListAPIView):
    serializer_class = ProjectSerializer
    queryset = Project.objects.all()
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class ProjectDetailsAPI(generics.RetrieveAPIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    lookup_field = 'id'
