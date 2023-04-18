
from django.contrib import admin
from django.urls import path, include

from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi


schema_view = get_schema_view(
    openapi.Info(
        title="Vāstu - Real Estate App",
        default_version='v1',
        description="this is an app that allows property owners to lsit their properies for sale or rent.",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="emmakolade@gmail.com"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
)


urlpatterns = [
    path('admin/', admin.site.urls),
    # path('authapp/', include('aut'))
    path('', schema_view.with_ui('swagger',
                                 cache_timeout=0), name='schema-swagger-ui'),


]
