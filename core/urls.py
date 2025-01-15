from django.contrib import admin
from django.urls import path, include
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework_simplejwt import views as jwt_views


schema_view = get_schema_view(
    openapi.Info(
        title="API Documentation",
        default_version='v1',
        description="API documentation with Swagger UI",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="jacksoncypriano@hotmail.com.com"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    #permission_classes=[IsAuthenticated],
)

urlpatterns = [
    path('accounts/', include('apps.accounts.urls')),
    path('programmers/', include('apps.programmers.urls')),
    path('projects/', include('apps.projects.urls')),
    path('technologies/', include('apps.technologies.urls')),
    path('api/token/', jwt_views.TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),
    path('documentation/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]
