from django.utils import timezone

from apps.projects.models import Project
from apps.choices import ProjectStatus
from celery import shared_task
import logging

logger = logging.getLogger(__name__)

@shared_task
def mark_project_as_late():
    now = timezone.now()
    projects = Project.objects.all().exclude(status__in=[ProjectStatus.LATE, ProjectStatus.DONE])

    for project in projects:
        if now.date() > project.end_date:
            project.status = ProjectStatus.LATE
            project.save()
