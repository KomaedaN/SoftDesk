from django.contrib import admin
from projects.models import Projects, Contributors, Issue, Comment


class ContributorAdmin(admin.ModelAdmin):
    list_display = ('id', 'project_id', 'user_id')


admin.site.register(Projects)
admin.site.register(Contributors, ContributorAdmin)
admin.site.register(Issue)
admin.site.register(Comment)
