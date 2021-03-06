from django.contrib import admin
from .models import Todo, Profile, Comments, GroupTask, Groups


class TodoAdmin(admin.ModelAdmin):
    list_display = ('id', 'author', 'title', 'description', 'date', 'done')
    list_display_links = ('id', 'title')
    search_fields = ('id', 'title', 'description')
    list_editable = ('done', )
    list_filter = ('done', )


class CommentAdmin(admin.ModelAdmin):
    list_display = ('id', 'author', 'text', 'todo')
    list_display_links = ('author', 'text')


class GroupTaskAdmin(admin.TabularInline):
    model = Groups.group_tasks.through


class GroupsAdmin(admin.ModelAdmin):
    list_display = ('name', 'admin')
    list_display_links = ('admin', )
    inlines = (GroupTaskAdmin,)


class GroupsTaskAdmin(admin.ModelAdmin):
    list_display = ('id', 'creator', 'worker', 'task_title', 'deadline', 'status')
    list_display_links = ('worker', 'task_title')


class ProfileAdmin(admin.ModelAdmin):
    list_display = ('id', 'username')


admin.site.register(Todo, TodoAdmin)
admin.site.register(Profile, ProfileAdmin)
admin.site.register(Comments, CommentAdmin)
admin.site.register(Groups, GroupsAdmin)
admin.site.register(GroupTask, GroupsTaskAdmin)
