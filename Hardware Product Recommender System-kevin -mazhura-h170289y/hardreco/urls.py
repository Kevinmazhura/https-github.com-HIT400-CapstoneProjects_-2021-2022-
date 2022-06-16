"""allbachelor URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
from django.urls import re_path as url
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from . import views
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from shop import views as shop_views

urlpatterns = [
    path('', shop_views.index, name="mainpage"),
    path('auth', include('django.contrib.auth.urls')),
    path('admin/', admin.site.urls),
    path('shop/', include('shop.urls')),
    path('blog/', include('blog.urls')),
    path('about/', views.about, name="about"),
    url(r'^shop/', include(('shop.urls', 'shop'), namespace='shop')),
    path('profiles/', include('profiles.urls',namespace='profiles')),
    path(r'markdownx/', include('markdownx.urls')),
    path('order/', include('order.urls',namespace='order')),
    path('tfidf/', include('tfidf.urls')),
    path('matrixfactorization/', include('matrixfactorization.urls')),
    url(r'^Scrapper/', include('scrapper.urls',namespace='scrapper')),
    url(r'^app/', include('app.urls')),
]
# if settings.DEBUG:
#     urlpatterns += static(settings.MEDIA_URL, document_root= settings.MEDIA_ROOT)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
else:
    urlpatterns += staticfiles_urlpatterns()