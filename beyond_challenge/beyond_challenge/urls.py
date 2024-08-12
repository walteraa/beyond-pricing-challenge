"""
URL configuration for beyond_challenge project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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
from django.urls import path
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

from dynamic_pricing.views.listing_calendar_view import ListingCalendarView
from dynamic_pricing.views.listing_details_view import ListingDetailsView
from dynamic_pricing.views.listing_view import ListingView



schema_view = get_schema_view(
   openapi.Info(
      title="Dynamic Pricing API",
      default_version='v0',
      description="This is the documentation for Beyond dynamic pricing test",
      terms_of_service="",
      contact=openapi.Contact(email="walter.arruda.alvest@gmail.com"),
      license=openapi.License(name="MIT License"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("listings", ListingView.as_view()),
    path("listings/<uuid:listing_id>", ListingDetailsView.as_view()),
    path("listings/<uuid:listing_id>/calendar", ListingCalendarView.as_view()),
    path('swagger<format>/', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]
