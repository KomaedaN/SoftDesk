from django.contrib import admin
from projects.models import Projects, Contributors, Issue, Comment


admin.site.register(Projects)
admin.site.register(Contributors)
admin.site.register(Issue)
admin.site.register(Comment)
