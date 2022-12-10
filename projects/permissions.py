from rest_framework.permissions import BasePermission
from projects.models import Projects, Contributors, Issue, Comment


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
        action_create = ['create', 'list']
        action_restriction = ['update', 'destroy']

        if view.action in action_restriction:
            current_user = request.user
            current_issue = Issue.objects.get(pk=view.kwargs['pk'])

            if current_user == current_issue.author_user_id:
                return True
            else:
                return False

        elif view.action in action_create:
            user_list = []
            current_project = Projects.objects.get(pk=view.kwargs['project_pk'])
            current_contributors = Contributors.objects.filter(project_id=current_project)

            for user in current_contributors:
                contributor = user.user_id
                user_list.append(contributor)

            if request.user in user_list:
                return True
            else:
                return False


class CommentsPermission(BasePermission):

    def has_permission(self, request, view):
        action = ['list', 'create', 'retrieve']
        action_restriction = ['update', 'destroy']

        if view.action in action:
            current_issue = Issue.objects.get(pk=view.kwargs['issue_pk'])
            current_project = Projects.objects.get(pk=view.kwargs['project_pk'])
            if current_project == current_issue.project_id:
                user_list = []
                current_contributors = Contributors.objects.filter(project_id=current_project)
                for i in range(len(current_contributors)):
                    contributor = current_contributors[i].user_id
                    user_list.append(contributor)
                if request.user in user_list:
                    return True
                else:
                    return False
            else:
                return False

        elif view.action in action_restriction:
            current_comment = Comment.objects.get(pk=view.kwargs['pk'])
            if current_comment.author_user_id == request.user:
                return True
            else:
                return False
