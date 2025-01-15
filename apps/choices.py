from django.db import models

class ProjectStatus(models.TextChoices):
    PLANNED = 'PLANNED', 'Planned'
    IN_PROGRESS = 'IN_PROGRESS', 'In Progress'
    LATE = 'LATE', 'Late'
    DONE = 'DONE', 'Done'
