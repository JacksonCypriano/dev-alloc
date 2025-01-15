from django.db import models
from django.core.exceptions import ValidationError

from apps.technologies.models import Technology


class Programmer(models.Model):
    name = models.CharField(max_length=128, unique=True)
    technology = models.JSONField(blank=True, null=True)

    def get_technology_list(self):
        return self.technology or []

    def set_technology_list(self, technology_list):
        valid_technologies = self.get_technology_list()

        for technology in technology_list:
            if isinstance(technology, str):
                try:
                    tech = Technology.objects.get(name=technology)
                    valid_technologies.append(tech.name)
                except Technology.DoesNotExist:
                    raise ValidationError(f"The technology '{technology}' does not exist.")
            elif isinstance(technology, dict):
                valid_technologies.append(technology)
            else:
                raise ValidationError("Each item in the technology list must be either a string or an object.")

        self.technology = valid_technologies
        self.save()

    def __str__(self):
        technology_names = (
            [tech if isinstance(tech, dict) else tech for tech in self.technology]
            if self.technology else None
        )
        tech_list = ", ".join(technology_names) if technology_names else "No technologies assigned"
        return f"Programmer: {self.name}, Technologies: {tech_list}"

    class Meta:
        verbose_name = "Programmer"
        verbose_name_plural = "Programmers"