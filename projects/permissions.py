from rest_framework.permissions import BasePermission
from projects.models import Projects, Contributors, Issue


class ProjectPermission(BasePermission):

    def has_permission(self, request, view):
        action = ['create', 'retrieve', 'list']
        action_restriction = ['update', 'destroy']

        if view.action in action_restriction:
            current_user = request.user
            current_project = Projects.objects.get(pk=view.kwargs['pk'])
            if current_user == current_project.author_user_id:
                return True
            else:
                return False

        elif view.action in action:
            return True

        else:
            return False


class ContributorPermission(BasePermission):

    def has_permission(self, request, view):
        action = []


class IssuePermission(BasePermission):

    def has_permission(self, request, view):
        action = ['list']
        action_create = ['create']
        action_restriction = ['update', 'destroy']
        if view.action in action:
            return True

        elif view.action in action_restriction:
            current_user = request.user
            current_issue = Issue.objects.get(pk=view.kwargs['pk'])
            if current_user == current_issue.author_user_id:
                return True
            else:
                return False
