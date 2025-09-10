from django.contrib import admin
from .models import Project


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ['name', 'start_date', 'equipment_sales_count', 'total_value', 'created_at']
    list_filter = ['start_date', 'created_at']
    search_fields = ['name', 'description']
    readonly_fields = ['created_at', 'updated_at', 'total_value', 'equipment_sales_count']
    
    fieldsets = (
        ('Project Information', {
            'fields': ('name', 'start_date', 'description')
        }),
        ('Statistics', {
            'fields': ('total_value', 'equipment_sales_count'),
            'classes': ('collapse',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
