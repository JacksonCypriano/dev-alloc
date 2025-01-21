from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Programmer
from .serializers import ProgrammerSerializer
from apps.technologies.models import Technology
from apps.pagination import DefaultPagination

import logging

logger = logging.getLogger("__name__")


class ProgrammerViewSet(viewsets.ModelViewSet):
    queryset = Programmer.objects.all()
    serializer_class = ProgrammerSerializer
    pagination_class = DefaultPagination
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = super().get_queryset()
        filter_params = {}

        for param, value in self.request.query_params.items():
            if param in [field.name for field in Programmer._meta.fields]:
                filter_params[param] = value
            elif '__' in param and param.split('__')[0] in [field.name for field in Programmer._meta.fields]:
                filter_params[param] = value

        if filter_params:
            queryset = queryset.filter(**filter_params)

        return queryset

    def update(self, request, *args, **kwargs):
        programmer = self.get_object()
        serializer = self.get_serializer(programmer, data=request.data, partial=False)
        
        if serializer.is_valid():
            technologies_data = request.data.get('technology', [])
            
            technologies = []
            for tech_name in technologies_data:
                try:
                    technology = Technology.objects.get(name=tech_name)
                    technologies.append(technology.name)
                except Technology.DoesNotExist:
                    return Response(
                        {"error": f"The technology '{tech_name}' does not exist. Please create it before assigning."},
                        status=status.HTTP_400_BAD_REQUEST
                    )
            programmer.set_technology_list(technologies)

            self.perform_update(serializer)

            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def partial_update(self, request, *args, **kwargs):
        programmer = self.get_object()
        serializer = self.get_serializer(programmer, data=request.data, partial=True)
        if serializer.is_valid():
            technologies_data = request.data.get('technology', [])
            technologies = []
            for tech_name in technologies_data:
                try:
                    technology = Technology.objects.get(name=tech_name)
                    technologies.append(technology.name)
                except Technology.DoesNotExist:
                    return Response(
                        {"error": f"The technology '{tech_name}' does not exist. Please create it before assigning."},
                        status=status.HTTP_400_BAD_REQUEST
                    )
            programmer.set_technology_list(technologies)
            programmer.save()
            self.perform_update(serializer)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
