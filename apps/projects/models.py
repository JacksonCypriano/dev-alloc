from django.db import models
from django.db.models import Sum
from django.core.exceptions import ValidationError
from decimal import Decimal

from apps.choices import ProjectStatus
from apps.technologies.models import Technology
from apps.programmers.models import Programmer


class Project(models.Model):
    name = models.CharField(max_length=128, unique=True)
    start_date = models.DateField()
    end_date = models.DateField()
    required_technologies = models.JSONField()
    status = models.CharField(choices=ProjectStatus.choices, default=ProjectStatus.PLANNED)

    def get_technology_list(self):
        return self.required_technologies or []

    def set_technology_list(self, technology_list):
        valid_technologies = self.required_technologies or []

        for technology in technology_list:
            if isinstance(technology, str):
                try:
                    tech = Technology.objects.get(name=technology)
                    if tech not in valid_technologies:
                        valid_technologies.append(tech)
                except Technology.DoesNotExist:
                    raise ValidationError(f"The technology '{technology}' does not exist.")
            elif isinstance(technology, dict):
                if technology not in valid_technologies:
                    valid_technologies.append(technology)
            else:
                raise ValidationError("Each item in the technology list must be either a string or an object.")

        self.required_technologies = valid_technologies
        self.save()

    def __str__(self):
        technologies = ", ".join([tech['name'] if isinstance(tech, dict) else tech for tech in self.required_technologies])
        return f"Project: {self.name}, Start Date: {self.start_date}, End Date: {self.end_date}, Required Technologies: {technologies}"

    class Meta:
        verbose_name = "Project"
        verbose_name_plural = "Projects"

class ProjectAllocation(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='allocations')
    developer = models.ForeignKey(Programmer, on_delete=models.CASCADE, related_name='allocations')
    hours = models.DecimalField(max_digits=5, decimal_places=2)

    def clean(self):
        required_technologies = self.project.required_technologies
        developer_technologies = self.developer.get_technology_list()

        if not any(tech in developer_technologies for tech in required_technologies):
            print("Validation error raised: Developer does not have at least one required technology for this project.")
            raise ValidationError(
                {'__all__': ['Developer does not have at least one required technology for this project.']}
            )
        
        total_allocated_hours = ProjectAllocation.objects.filter(project=self.project).aggregate(total=Sum('hours'))['total'] or Decimal(0)
        if total_allocated_hours + self.hours > Decimal(80):
            print("Validation error raised: Total allocated hours exceed project limit.")
            raise ValidationError(
                {'__all__': ['The total allocated hours for the project cannot exceed the total project hours (80 hours).']}
            )

    class Meta:
        verbose_name = "Developer Allocation"
        verbose_name_plural = "Developer Allocations"
        unique_together = ['project', 'developer']

    def __str__(self):
        return f"{self.developer.name} allocated to {self.project.name} for {self.hours} hours"
