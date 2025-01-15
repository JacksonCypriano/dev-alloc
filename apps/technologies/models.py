from django.db import models


class Technology(models.Model):
    name = models.CharField(max_length=18, unique=True)

    class Meta:
        verbose_name = "Technology"
        verbose_name_plural = "Technologies"

    def __str__(self):
        return f"{self.name}"
