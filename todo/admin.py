from django.contrib import admin
from .models import Todo, Profile


class TodoAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'description', 'date', 'done')
    list_display_links = ('id', 'title')
    search_fields = ('id', 'title', 'description')
    list_editable = ('done', )
    list_filter = ('done', )


admin.site.register(Todo, TodoAdmin)
admin.site.register(Profile)
