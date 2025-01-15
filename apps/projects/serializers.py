from rest_framework import serializers
from .models import Project, ProjectAllocation
from apps.choices import ProjectStatus
from django.utils import timezone
from decimal import Decimal
from django.db.models import Sum
from datetime import datetime

class ProjectSerializer(serializers.ModelSerializer):
    required_technologies = serializers.JSONField()
    status = serializers.ChoiceField(choices=ProjectStatus.choices)

    class Meta:
        model = Project
        fields = ['id', 'name', 'start_date', 'end_date', 'required_technologies', 'status']

    def validate_required_technologies(self, value):
        if not isinstance(value, list):
            raise serializers.ValidationError("required_technologies must be a list.")
        for tech in value:
            if not isinstance(tech, str):
                raise serializers.ValidationError(f"Each technology must be a string, got {type(tech)}.")
        return value


class ProjectAllocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectAllocation
        fields = ['id', 'project', 'developer', 'hours']

    def validate_developer(self, value):
        developer = value
        project_id = self.initial_data.get('project')
        project = Project.objects.get(id=project_id)

        if not project_id:
            raise serializers.ValidationError("Project not specified.")

        required_technologies = project.get_technology_list()
        if not required_technologies:
            raise serializers.ValidationError(f"The project {project.name} does not require any technologies.")

        developer_technologies = developer.get_technology_list()

        if not any(tech in developer_technologies for tech in required_technologies):
            raise serializers.ValidationError(f"The developer {developer.name} does not have the technologies required by the project.")

        return value

    def validate_hours(self, value):
        project_id = self.initial_data.get('project')
        if not project_id:
            raise serializers.ValidationError("Project not specified.")
        
        project = Project.objects.get(id=project_id)
        start_date = project.start_date
        end_date = project.end_date

        if not start_date or not end_date:
            raise serializers.ValidationError("The project does not have a valid time frame.")

        if timezone.now() < timezone.make_aware(datetime.combine(start_date, datetime.min.time())) or timezone.now() > timezone.make_aware(datetime.combine(end_date, datetime.min.time())):
            raise serializers.ValidationError(f"Hours cannot be allocated outside the project's time frame ({start_date} to {end_date}).")

        return value

    def validate(self, attrs):
        project = attrs.get('project')
        hours = attrs.get('hours')

        if not project:
            raise serializers.ValidationError({"project": "Project not specified."})

        start_date = project.start_date
        end_date = project.end_date

        if start_date and end_date:
            project_duration = end_date - start_date
            total_project_hours = Decimal(project_duration.days * 8)
        else:
            raise serializers.ValidationError({"project": "Invalid project date range."})

        total_allocated_hours = ProjectAllocation.objects.filter(project=project).aggregate(total_hours=Sum('hours'))['total_hours'] or Decimal(0)

        if total_allocated_hours + hours > total_project_hours:
            raise serializers.ValidationError({
                "non_field_errors": [f"The total allocated hours for the project cannot exceed the total project hours ({total_project_hours} hours)."]
            })

        return attrs