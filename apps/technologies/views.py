from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from apps.technologies.models import Technology
from apps.technologies.serializers import TechnologySerializer
from apps.pagination import DefaultPagination

class TechnologyViewSet(viewsets.ModelViewSet):
    permission_class = [IsAuthenticated]
    serializer_class = TechnologySerializer
    pagination_class = DefaultPagination
    queryset = Technology.objects.all()

    def get_queryset(self):
        queryset = super().get_queryset()
        filter_params = {}

        for param, value in self.request.query_params.items():
            if param in [field.name for field in Technology._meta.fields]:
                filter_params[param] = value
            elif '__' in param and param.split('__')[0] in [field.name for field in Technology._meta.fields]:
                filter_params[param] = value

        if filter_params:
            queryset = queryset.filter(**filter_params)

        return queryset
