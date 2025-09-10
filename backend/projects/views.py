from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Project
from .serializers import ProjectSerializer, ProjectTimelineSerializer


class ProjectViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing Projects.
    Provides CRUD operations for projects and timeline data.
    """
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    
    def get_serializer_class(self):
        if self.action == 'timeline':
            return ProjectTimelineSerializer
        return ProjectSerializer
    
    @action(detail=True, methods=['get'])
    def timeline(self, request, pk=None):
        """
        Get the timeline for a specific project.
        Returns data formatted for gantt chart visualization.
        """
        project = self.get_object()
        serializer = self.get_serializer(project)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def timelines(self, request):
        """
        Get timelines for all projects.
        Returns data formatted for gantt chart visualization.
        """
        projects = self.get_queryset()
        serializer = ProjectTimelineSerializer(projects, many=True)
        return Response(serializer.data)
