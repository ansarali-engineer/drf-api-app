from django.contrib import admin
from django.urls import path, include, re_path

from rest_framework import permissions

from user.views import JWTLoginView, JWTTokenRefreshView, LoginView

from drf_yasg.views import get_schema_view
from drf_yasg import openapi


schema_view = get_schema_view(
    openapi.Info(
        title="Final Assessment",
        default_version="v1",
        description="CRM API",
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)


urlpatterns = [
    path('admin/', admin.site.urls),

    path(
        'api/api-token-auth/',
        LoginView.as_view(),
        name='api_token_auth'
    ),

    path('api/', include('branch.urls')),
    path('api/', include('Role.urls')),
    path('api/', include('user.urls')),
    path('api/', include('customer.urls')),
    path('api/', include('lead.urls')),
    path('api/', include('leadactivity.urls')),

    path(
        'api/token/',
        JWTLoginView.as_view(),
        name='token_obtain_pair'
    ),

    path(
        'api/token/refresh/',
        JWTTokenRefreshView.as_view(),
        name='token_refresh'
    ),

    re_path(
        r'^swagger(?P<format>\.json|\.yaml)$',
        schema_view.without_ui(cache_timeout=0),
        name='schema-json'
    ),

    path(
        'swagger/',
        schema_view.with_ui('swagger', cache_timeout=0),
        name='schema-swagger-ui'
    ),

    path(
        'redoc/',
        schema_view.with_ui('redoc', cache_timeout=0),
        name='schema-redoc'
    ),
]


