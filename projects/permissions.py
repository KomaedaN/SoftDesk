from rest_framework.permissions import BasePermission
from projects.models import Projects, Contributors, Issue, Comment
from authentication.models import User
from rest_framework.response import Response


class ProjectPermission(BasePermission):

    def has_permission(self, request, view):
        action = ['create', 'retrieve', 'list']
        action_restriction = ['update', 'destroy']

        if view.action in action_restriction:
            current_project = Projects.objects.get(pk=view.kwargs['pk'])
            if request.user == current_project.author_user_id:
                # verify if current user is the project owner
                return True
            else:
                return False

        elif view.action in action:
            return True

        else:
            return False


class ContributorPermission(BasePermission):

    def has_permission(self, request, view):
        action_list = ['list']
        action_create = ['create']
        action_destroy = ['destroy']

        if view.action in action_list:
            current_project = Projects.objects.get(pk=view.kwargs['project_pk'])
            contributors_list = Contributors.objects.filter(project_id=current_project)
            for user in contributors_list:
                contributor = user.user_id
                if contributor == request.user:
                    # verify if current user is a contributor from this project
                    return True
            return False

        elif view.action in action_create:
            try:
                current_project = Projects.objects.get(pk=view.kwargs['project_pk'])
                contributors_list = Contributors.objects.filter(project_id=current_project)
                current_contributors = Contributors.objects.get(project_id=current_project, permission='AUTHOR')
                if current_contributors.user_id == request.user:
                    # verify if current user is the AUTHOR
                    for user in contributors_list:
                        contributor = user.user_id

                        if contributor == User.objects.get(username=request.POST['user_id']):
                            # verify if user_id is already a contributor from this project
                            return False
                    return True
            except:
                return False

        elif view.action in action_destroy:
            try:
                current_project = Projects.objects.get(pk=view.kwargs['project_pk'])
                current_contributors = Contributors.objects.get(project_id=current_project, permission='AUTHOR')
                if current_contributors.user_id == request.user:
                    # verify if current user is the AUTHOR
                    return True
            except:
                return False

        else:
            return False


class IssuePermission(BasePermission):

    def has_permission(self, request, view):
        action_create = ['create', 'list']
        action_restriction = ['update', 'destroy']

        if view.action in action_restriction:
            current_user = request.user
            current_issue = Issue.objects.get(pk=view.kwargs['pk'])

            if current_user == current_issue.author_user_id:
                # verify if current user is the author from this issue
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
                # verify if current user is a contributor from this project
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
                # verify if current issue is from the current project
                user_list = []
                current_contributors = Contributors.objects.filter(project_id=current_project)
                for i in range(len(current_contributors)):
                    contributor = current_contributors[i].user_id
                    user_list.append(contributor)
                if request.user in user_list:
                    # verify if current user is a contributor from this project
                    return True
                else:
                    return False
            else:
                return False

        elif view.action in action_restriction:
            current_comment = Comment.objects.get(pk=view.kwargs['pk'])
            if current_comment.author_user_id == request.user:
                # verify if current user is the comment owner
                return True
            else:
                return False
