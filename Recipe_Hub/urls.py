from django.contrib import admin
from django.urls import path, include, re_path
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
    openapi.Info(
        title="Recipe API",
        default_version='v1',
        description="Interactive API documentation for the Recipe app",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="nahomhulum@email.com"),
        license=openapi.License(name="MIT License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
    authentication_classes=[],
)

# Define OAuth2 manually (Swagger 2.0 style)
schema_view.security_definitions = {
    'oauth2': {
        'type': 'oauth2',
        'flow': 'password',
        'tokenUrl': '/api/token/',
        'scopes': {}
    }
}

# Optionally apply OAuth2 globally
schema_view.security = [{'oauth2': []}]

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('api.urls')),
    path('api-auth/', include('rest_framework.urls')),  # Optional for browsable API login/logout

    # Swagger endpoints
    re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]

# Static files
from django.conf import settings
from django.conf.urls.static import static

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
