from django.contrib import admin
from .models import Node

@admin.register(Node)
class NodeAdmin(admin.ModelAdmin):
    list_display = ('id', 'ip', 'location', 'status', 'last_update')
    list_filter = ('status', 'location')
    search_fields = ('ip', 'location')
