from django.urls import path
from drf_yasg import openapi
from drf_yasg.generators import OpenAPISchemaGenerator
from drf_yasg.views import get_schema_view
from rest_framework import permissions

from core.Utilities.JWTAuth import JWTAuthenticationScheme
from core.views.credential_management import list_credentials, create_credential, update_credential, \
    grant_access
from core.views.service import ServiceViewSet
from core.views.tags import TagViewSet, SingleTagViewSet
from core.views.user_management import register, login


class BearerTokenSchemaGenerator(OpenAPISchemaGenerator):
    def get_schema(self, request=None, public=False):
        schema = super().get_schema(request, public)
        schema.security_definitions = {
            'Bearer': {
                'type': 'apiKey',
                'name': 'Authorization',
                'in': 'header'
            }
        }
        schema.security = [{'Bearer': []}]
        return schema


schema_view = get_schema_view(
    openapi.Info(
        title="API Documentation",
        default_version='v1',
        description="API documentation with JWT authentication",
    ),
    public=True,
    permission_classes=[permissions.AllowAny, ],
    authentication_classes=[JWTAuthenticationScheme],
    generator_class=BearerTokenSchemaGenerator,
)

urlpatterns = [
    path('swagger<format>/', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),

    path('register/', register, name='register'),
    path('login/', login, name='login'),

    path('credentials/', list_credentials, name='list-credentials'),
    path('credentials/create/', create_credential, name='create-credential'),
    path('credentials/<int:pk>/update/', update_credential, name='update-credential'),
    path('credentials/<int:pk>/grant-access/', grant_access, name='grant-access'),

    path('services/', ServiceViewSet.as_view(), name='service-list-create'),
    path('services/<int:pk>/', SingleTagViewSet.as_view(), name='service-detail'),

    path('tags/', TagViewSet.as_view(), name='tag-list-create'),

    path('tags/<int:pk>/', SingleTagViewSet.as_view(), name='tag-detail'),

]
