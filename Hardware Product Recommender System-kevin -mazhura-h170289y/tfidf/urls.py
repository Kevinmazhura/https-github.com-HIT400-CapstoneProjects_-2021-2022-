from django.contrib import admin
from django.urls import path
from django.urls import include, re_path as url
from . import views

from django.conf import settings
from django.conf.urls.static import static
app_name = 'tfidf'

urlpatterns = [
    url(r'^recommendations/', views.recommendation, name='recommendations'),
    path('detail/<int:id>', views.detail, name='detail'),
    path('home', views.post_list, name='home'),
    url(r'^cosrecommendations/', views.get_suggestions, name='cosrecommendation'),
]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

