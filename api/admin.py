from django.contrib import admin
from .models import AppUser

admin.site.site_header = 'Repertoire Tracker Admin'

class AppUserAdmin(admin.ModelAdmin):
    list_display = ('username', 'display_name', 'created_at')
    readonly_fields = ('username', 'display_name', 'password', 'created_at', 'token')
    search_fields = ('username', 'display_name')
    
admin.site.register(AppUser, AppUserAdmin)
