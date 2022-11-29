from django.db import models
from django.conf import settings


class Projects(models.Model):
    TYPES = [
        ('BACKEND', 'Back-end'),
        ('FRONTEND', 'Front-end'),
        ('IOS', 'IOS'),
        ('ANDROID', 'Android')
    ]

    title = models.CharField(max_length=150)
    description = models.CharField(max_length=1500)
    type = models.CharField(max_length=15, choices=TYPES)
    author_user_id = models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='author')


class Contributors(models.Model):
    ROLES = [
        ('AUTHOR', 'AUTHOR'),
        ('CONTRIBUTOR', 'CONTRIBUTOR')
    ]

    user_id = models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    project_id = models.ForeignKey(to=Projects, on_delete=models.CASCADE, related_name='contributors')
    permission = models.CharField(max_length=20, choices=ROLES, default='CONTRIBUTOR')


class Issue(models.Model):
    PRIORITY = [
        ('LOW', 'Low'),
        ('MEDIUM', 'Medium'),
        ('HIGH', 'HIGH')
    ]

    STATUS = [
        ('TO DO', 'To do'),
        ('IN PROGRESS', 'In progress'),
        ('DONE', 'Done')
    ]

    TAG = [
        ('BUG', 'Bug'),
        ('IMPROVEMENT', 'Improvement'),
        ('TASK', 'Task')
    ]

    title = models.CharField(max_length=150)
    description = models.CharField(max_length=1500)
    tag = models.CharField(max_length=12, choices=TAG)
    priority = models.CharField(max_length=6, choices=PRIORITY, default='LOW')
    status = models.CharField(max_length=12, choices=STATUS, default='TO DO')
    project_id = models.ForeignKey(to=Projects, on_delete=models.CASCADE)
    author_user_id = models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    assignee_user_id = models.ForeignKey(to=Contributors, on_delete=models.CASCADE)
    created_time = models.DateTimeField(auto_now_add=True)


class Comment(models.Model):
    description = models.CharField(max_length=1500)
    author_user_id = models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    issue_id = models.ForeignKey(to=Issue, on_delete=models.CASCADE)
    created_time = models.DateTimeField(auto_now_add=True)
