from . import views
from django.conf.urls import  include
from django.urls import path,re_path as url
from django.contrib.auth import views as auth_views
from django.conf.urls.static import static
from django.conf import settings

app_name = 'profiles'


urlpatterns = [
    # path('accounts/', include('profiles.accounts.urls', namespace='accounts')),
    path('profiles/<slug:profile_slug>/change-password', views.change_password, name="change-password"),
    path('profiles/<slug:profile_slug>/edit', views.edit_profile, name="edit-profile"),
    path('profiles/<slug:profile_slug>/', views.profile, name="profile"),
    path('intrest/<slug:profile_slug>/', views.add_intrest, name="add_intrest"),
    
    path('', views.profiles, name="profiles"),
    path('profile/home', views.index, name="home")
    


] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)




