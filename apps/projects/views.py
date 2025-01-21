from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Project
from .serializers import ProjectSerializer
from apps.pagination import DefaultPagination

class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    pagination_class = DefaultPagination
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = super().get_queryset()
        filter_params = {}

        for param, value in self.request.query_params.items():
            if param in [field.name for field in Project._meta.fields]:
                filter_params[param] = value
            elif '__' in param and param.split('__')[0] in [field.name for field in Project._meta.fields]:
                filter_params[param] = value

        if filter_params:
            queryset = queryset.filter(**filter_params)

        return queryset
