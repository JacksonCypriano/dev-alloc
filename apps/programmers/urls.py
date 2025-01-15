from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ProgrammerViewSet

router = DefaultRouter()
router.register(r'', ProgrammerViewSet, basename='programmers')

urlpatterns = [
    path('', include(router.urls)),
]