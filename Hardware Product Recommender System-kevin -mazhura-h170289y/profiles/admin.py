from django.contrib import admin

from .models import Profile, ProfileIntrests
class ProfileAdmin(admin.ModelAdmin):
    # ...
    list_display = ['user', 'email', 'date_of_birth', 'slug']
    list_filter = ['user', 'email', 'date_of_birth', 'slug']
    list_editable = ['date_of_birth']
    readonly_fields = ('email','user','slug',)


admin.site.register(Profile, ProfileAdmin)
admin.site.register(ProfileIntrests)
