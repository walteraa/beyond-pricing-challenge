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

from dynamic_pricing.views.listing_details_view import ListingDetailsView
from dynamic_pricing.views.listing_view import ListingView

urlpatterns = [
    path("admin/", admin.site.urls),
    path("listings", ListingView.as_view()),
    path("listings/<uuid:listing_id>", ListingDetailsView.as_view())
]
