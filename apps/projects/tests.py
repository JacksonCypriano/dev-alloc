from django.test import TestCase
from apps.projects.models import Project
from apps.programmers.models import Programmer
from apps.projects.models import ProjectAllocation
from apps.technologies.models import Technology
from django.core.exceptions import ValidationError
from decimal import Decimal
from django.utils import timezone
from apps.projects.serializers import ProjectAllocationSerializer

class ProjectAllocationTests(TestCase):

    def setUp(self):
        self.technology1, _ = Technology.objects.get_or_create(name="Python")
        self.technology2, _ = Technology.objects.get_or_create(name="Django")
        self.technology3, _ = Technology.objects.get_or_create(name="Java")

        self.project, _ = Project.objects.get_or_create(
            name="Project 1",
            start_date=timezone.now(),
            end_date=timezone.now() + timezone.timedelta(days=10),
            required_technologies=[self.technology1.name, self.technology2.name]
        )

        self.developer, _ = Programmer.objects.get_or_create(name="Developer 1")
        self.developer.set_technology_list([self.technology1.name])

        self.allocation, _ = ProjectAllocation.objects.get_or_create(
            project=self.project,
            developer=self.developer,
            hours=Decimal(10)
        )

    def test_developer_technology_validation(self):
        try:
            self.allocation.full_clean()
        except ValidationError:
            self.fail("ValidationError raised when developer has required technology.")

    def test_developer_technology_validation_serializer(self):
        allocation_data = {
            'project': self.project.id,
            'developer': self.developer.id,
            'hours': Decimal(10)
        }

        serializer = ProjectAllocationSerializer(instance=self.allocation, data=allocation_data)

        self.assertTrue(serializer.is_valid())

    def test_developer_technology_validation_invalid(self):
        from django.core.exceptions import ValidationError
        invalid_developer, _ = Programmer.objects.get_or_create(name="Developer 3")
        invalid_developer.set_technology_list(["Java"])

        self.allocation.developer = invalid_developer

        with self.assertRaises(ValidationError) as cm:
            self.allocation.full_clean()

        self.assertIn(
            "Developer does not have at least one required technology for this project.",
            str(cm.exception)
        )

    def test_developer_technology_validation_invalid_serializer(self):
        invalid_developer, _ = Programmer.objects.get_or_create(name="Developer 3")
        invalid_developer.set_technology_list(["Java"])
        self.allocation.developer = invalid_developer

        allocation_data = {
            'project': self.project.id,
            'developer': invalid_developer.id,
            'hours': Decimal(10)
        }

        serializer = ProjectAllocationSerializer(instance=self.allocation, data=allocation_data)

        self.assertFalse(serializer.is_valid())

    def test_allocation_outside_project_period(self):
        allocation = ProjectAllocation(
            project=self.project,
            developer=self.developer,
            hours=Decimal(40)
        )

        with self.assertRaises(ValidationError):
            allocation.full_clean()

    def test_allocation_outside_project_period_serializer(self):
        from rest_framework.exceptions import ValidationError
        allocation_data = {
            'project': self.project.id,
            'developer': self.developer.id,
            'hours': Decimal(5)
        }

        self.project.start_date = timezone.now() + timezone.timedelta(days=15)
        self.project.end_date = timezone.now() + timezone.timedelta(days=20)

        allocation_data['hours'] = Decimal(100)

        serializer = ProjectAllocationSerializer(instance=self.allocation, data=allocation_data)

        with self.assertRaises(ValidationError):
            serializer.is_valid(raise_exception=True)


    def setUp_hours_limit(self):
        self.technology1, _ = Technology.objects.get_or_create(name="Python")
        self.project, _ = Project.objects.get_or_create(
            name="Project 1",
            start_date=timezone.now(),
            end_date=timezone.now() + timezone.timedelta(days=10),
            required_technologies=[self.technology1.name]
        )

        self.developer, _ = Programmer.objects.get_or_create(name="Developer 1")
        self.developer.set_technology_list([self.technology1.name])

        self.allocation1, _ = ProjectAllocation.objects.get_or_create(
            project=self.project,
            developer=self.developer,
            hours=Decimal(30)
        )

    def test_hours_limit_exceeded(self):
        from django.core.exceptions import ValidationError
        
        self.allocation.hours = Decimal("90")
        with self.assertRaises(ValidationError):
            self.allocation.full_clean()

    def test_hours_limit_exceeded_serializer(self):
        from rest_framework.exceptions import ValidationError
        allocation_data = {
            'project': self.project.id,
            'developer': self.developer.id,
            'hours': Decimal(90)
        }

        serializer = ProjectAllocationSerializer(instance=self.allocation, data=allocation_data)

        with self.assertRaises(ValidationError) as cm:
            serializer.is_valid(raise_exception=True)

        self.assertIn(
            "The total allocated hours for the project cannot exceed the total project hours",
            str(cm.exception)
        )
