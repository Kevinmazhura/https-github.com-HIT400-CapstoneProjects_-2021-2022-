"""
Definition of urls for HardwareStore.
"""

from datetime import datetime
from django.urls import path
from django.contrib import admin
from django.contrib.auth.views import LoginView, LogoutView
from app import forms, views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

from . import views
app_name = "scrapper"

urlpatterns = [
    path('', views.HalstedProducts, name='halsteds_products'),
    
    path('vaka', views.scrap_vaka, name='vaka'),
    path('HalstedProducts_by_category', views.HalstedProducts_by_category, name='HalstedProducts_by_category'),
    path('halsteds_categories', views.HalstedsCategories, name='halsteds_categories'),
]
