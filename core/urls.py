"""
URL configuration for core project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from core.health import main
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework.permissions import AllowAny
from django.urls import re_path

schema_view = get_schema_view(
    openapi.Info(
        title="Event Manager API",
        default_version='v1',
        description="""The event-manager-api is a rest API that provides an easy way
        to manage and track events. It allows users to create, update, and delete
        events, as well as view and search them.""",
        contact=openapi.Contact(email="alex.falcucci@gmail.com"),
    ),
    public=True,
    permission_classes=(AllowAny,),
)



urlpatterns = [
    path('admin/', admin.site.urls),
    path('health/', main.health),
    path('api/', include('authentication.urls')),
    path('api/', include('events.urls')),

    re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    re_path(r'^swagger/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    re_path(r'^redoc/$', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),

]
